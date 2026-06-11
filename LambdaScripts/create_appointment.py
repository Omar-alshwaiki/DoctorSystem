import boto3
import json
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

slots_table = dynamodb.Table('Slots')
appointments_table = dynamodb.Table('Appointments')

TOPIC_ARN = 'arn:aws:sns:us-east-1:211839440217:Yazan'

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST,OPTIONS"
}

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': ''}

    try:
        data = json.loads(event['body'])
        patient_name = data['patientName']
        symptoms = data['symptoms']
        slot_id = data['slotId']
        time_label = data['timeLabel']

        # 1. Look up availability using your primary partition key name: slot_id
        slot_item = slots_table.get_item(Key={'slot_id': slot_id})
        if 'Item' not in slot_item or slot_item['Item'].get('status') != 'available':
            return {
                'statusCode': 409,
                'headers': CORS_HEADERS,
                'body': json.dumps({'message': 'Slot is already booked'})
            }

        # 2. Create the appointment using your key: appointment_id
        appointment_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()

        appointments_table.put_item(Item={
            'appointment_id': appointment_id,
            'patientName': patient_name,
            'symptoms': symptoms,
            'slot_id': slot_id,
            'slot': time_label, # Saved as time string for clean UI listing
            'status': 'Pending',
            'createdAt': created_at
        })

        # 3. Mark the slot string status as 'booked'
        slots_table.update_item(
            Key={'slot_id': slot_id},
            UpdateExpression="SET #s = :b",
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':b': 'booked'}
        )

        # 4. Fire SNS Notification
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject='New Appointment Booked',
            Message=(
                f"A new appointment has been booked:\n"
                f"Patient: {patient_name}\n"
                f"Slot Window: {time_label}\n"
                f"Symptoms: {symptoms}\n"
                f"Time: {created_at}"
            )
        )

        return {
            'statusCode': 201,
            'headers': CORS_HEADERS,
            'body': json.dumps({
                'message': 'Appointment created successfully',
                'appointmentId': appointment_id
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e)})
        }
