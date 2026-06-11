import boto3
import json
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

slots_table = dynamodb.Table('Slots')
appointments_table = dynamodb.Table('Appointments')

TOPIC_ARN = 'arn:aws:sns:us-east-1:211839440217:Yazan'

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        patient_name = data['patientName']
        symptoms = data['symptoms']
        slot = data['slot']

        # Check if the slot is available
        slot_item = slots_table.get_item(Key={'slot': slot})
        if 'Item' not in slot_item or slot_item['Item']['isBooked']:
            return {
                'statusCode': 409,
                'body': json.dumps({'message': 'Slot is already booked'})
            }

        # Create the appointment
        appointment_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()

        appointments_table.put_item(Item={
            'appointmentId': appointment_id,
            'patientName': patient_name,
            'symptoms': symptoms,
            'slot': slot,
            'status': 'Pending',
            'createdAt': created_at
        })

        # Mark the slot as booked
        slots_table.update_item(
            Key={'slot': slot},
            UpdateExpression="SET isBooked = :b",
            ExpressionAttributeValues={':b': True}
        )

        # Send SNS Notification
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject='New Appointment Booked',
            Message=(
                f"A new appointment has been booked:\n"
                f"Patient: {patient_name}\n"
                f"Slot: {slot}\n"
                f"Symptoms: {symptoms}\n"
                f"Time: {created_at}"
            )
        )

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Appointment created successfully',
                'appointmentId': appointment_id
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
