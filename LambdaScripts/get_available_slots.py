import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Slots')

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,OPTIONS"
}

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': ''}
        
    try:
        # Match your schema where status attribute string equals 'available'
        response = table.scan(
            FilterExpression='#s = :status_val',
            ExpressionAttributeNames={'#s': 'status'}, # status is an AWS reserved keyword
            ExpressionAttributeValues={':status_val': 'available'}
        )
        slots = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                **CORS_HEADERS
            },
            'body': json.dumps(slots)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e)})
        }
