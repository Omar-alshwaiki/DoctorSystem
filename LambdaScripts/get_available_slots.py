import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Slots')

def lambda_handler(event, context):
    try:
        response = table.scan(
            FilterExpression='isBooked = :b',
            ExpressionAttributeValues={':b': False}
        )
        slots = response.get('Items', [])
        return {
            'statusCode': 200,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps(slots)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
