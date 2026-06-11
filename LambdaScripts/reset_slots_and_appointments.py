import boto3

dynamodb = boto3.resource('dynamodb')
slots_table = dynamodb.Table('Slots')
appointments_table = dynamodb.Table('Appointments')

SLOTS = ["8 - 9", "9 - 10", "10 - 11", "11 - 12", "12 - 1"]

def lambda_handler(event, context):
    try:
        # 1. Scan and delete all current slots
        slots_response = slots_table.scan()
        existing_slots = slots_response.get('Items', [])

        with slots_table.batch_writer() as batch:
            for slot in existing_slots:
                batch.delete_item(Key={'slot': slot['slot']})

        # 2. Re-insert default slots
        with slots_table.batch_writer() as batch:
            for slot in SLOTS:
                batch.put_item(Item={
                    'slot': slot,
                    'isBooked': False
                })

        # 3. Scan and delete all appointments
        appointments_response = appointments_table.scan()
        existing_appointments = appointments_response.get('Items', [])

        with appointments_table.batch_writer() as batch:
            for appointment in existing_appointments:
                batch.delete_item(Key={'appointmentId': appointment['appointmentId']})

        return {
            'statusCode': 200,
            'body': 'Slots and appointments reset successfully.'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
