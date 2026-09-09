import json
import os
import uuid
from datetime import datetime
import boto3

# 1. تهيئة عملاء خدمات AWS (Boto3 SDK)
comprehend = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# 2. جلب أسماء الجداول والـ ARNs من المتغيرات البيئية (Environment Variables)
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'ContactFormMessages')
CRITICAL_SNS_ARN = os.environ.get('CRITICAL_SNS_TOPIC_ARN')
GENERAL_SNS_ARN = os.environ.get('GENERAL_SNS_TOPIC_ARN')

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    # إعدادات الـ CORS لتعمل مع أي Frontend (CloudFront / S3)
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        "Content-Type": "application/json"
    }
    
    # التعامل مع طلبات Preflight (OPTIONS Request)
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight successful'})
        }

    try:
        # قراءة وتفكيك نص الطلب الوارد من API Gateway
        body = json.loads(event.get('body', '{}'))
        name = body.get('name', 'Anonymous')
        email = body.get('email', 'No Email')
        subject = body.get('subject', 'General Inquiry')
        message = body.get('message', '')

        if not message.strip():
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Message content cannot be empty'})
            }

        # 3. استخدام Amazon Comprehend لتحليل مشاعر الرسالة (AI Analysis)
        sentiment = 'NEUTRAL'
        try:
            comprehend_response = comprehend.detect_sentiment(
                Text=message,
                LanguageCode='en'
            )
            sentiment = comprehend_response.get('Sentiment', 'NEUTRAL')
        except Exception as comp_err:
            print(f"Comprehend Analysis Error: {str(comp_err)}")

        # 4. تحديد الأولوية وتوجيه الإشعارات بناءً على نتيجة الذكاء الاصطناعي
        priority = 'LOW'
        target_sns_arn = GENERAL_SNS_ARN
        
        # الكلمات المفتاحية الحرجة
        urgent_keywords = ['urgent', 'hacked', 'down', 'broken', 'critical', 'error']
        message_lower = message.lower()

        if sentiment == 'NEGATIVE' or any(word in message_lower for word in urgent_keywords):
            priority = 'CRITICAL'
            target_sns_arn = CRITICAL_SNS_ARN
        elif sentiment == 'POSITIVE':
            priority = 'FEEDBACK'

        # 5. حفظ البيانات في Amazon DynamoDB
        message_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'

        item = {
            'message_id': message_id,
            'timestamp': timestamp,
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'sentiment': sentiment,
            'priority': priority
        }
        
        table.put_item(Item=item)

        # 6. إرسال تنبيه عبر Amazon SNS إذا كان معرّف التنبيه موجوذاً
        if target_sns_arn:
            sns_message = (
                f"NEW CONTACT FORM SUBMISSION\n"
                f"---------------------------\n"
                f"Priority: {priority}\n"
                f"Sentiment: {sentiment}\n"
                f"From: {name} ({email})\n"
                f"Subject: {subject}\n"
                f"Date: {timestamp}\n\n"
                f"Message:\n{message}"
            )
            
            sns.publish(
                TopicArn=target_sns_arn,
                Subject=f"[{priority}] New Message from {name}",
                Message=sns_message
            )

        # 7. إرجاع استجابة نجاح للمستخدم
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'message': 'Your message has been processed successfully.',
                'data': {
                    'message_id': message_id,
                    'sentiment': sentiment,
                    'priority': priority
                }
            })
        }

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error processing your request.'})
        }