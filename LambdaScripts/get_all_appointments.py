import boto3
import json

dynamodb = boto3.resource('dynamodb')
appointments_table = dynamodb.Table('Appointments')

def lambda_handler(event, context):
    try:
        response = appointments_table.scan()
        appointments = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps(appointments)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({ 'error': str(e) })
        }
