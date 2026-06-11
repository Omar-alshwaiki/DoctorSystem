import boto3
import json

dynamodb = boto3.resource('dynamodb')
appointments_table = dynamodb.Table('Appointments')

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,OPTIONS"
}

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': ''}

    try:
        response = appointments_table.scan()
        appointments = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': { 
                'Content-Type': 'application/json',
                **CORS_HEADERS
            },
            'body': json.dumps(appointments)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({ 'error': str(e) })
        }
