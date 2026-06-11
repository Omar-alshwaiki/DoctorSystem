import boto3
import json

dynamodb = boto3.resource('dynamodb')
appointments_table = dynamodb.Table('Appointments')

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': ''
        }

    try:
        appointment_id = event.get('pathParameters', {}).get('appointmentId')
        if not appointment_id:
            return {
                'statusCode': 400,
                'headers': { "Access-Control-Allow-Origin": "*" },
                'body': json.dumps({ 'message': 'Missing appointmentId in path.' })
            }

        raw_body = event.get('body', '{}')
        body = json.loads(raw_body) if isinstance(raw_body, str) else raw_body

        new_status = body.get('status')
        if new_status not in ['Pending', 'In Progress', 'Completed']:
            return {
                'statusCode': 400,
                'headers': { "Access-Control-Allow-Origin": "*" },
                'body': json.dumps({ 'message': 'Invalid status value.' })
            }

        appointments_table.update_item(
            Key={'appointmentId': appointment_id},
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':s': new_status}
        )

        return {
            'statusCode': 200,
            'headers': { "Access-Control-Allow-Origin": "*" },
            'body': json.dumps({ 'message': 'Status updated successfully.' })
        }

    except Exception as e:
        print("EVENT:", json.dumps(event))
        return {
            'statusCode': 500,
            'headers': { "Access-Control-Allow-Origin": "*" },
            'body': json.dumps({ 'error': str(e) })
        }
