import boto3

dynamodb = boto3.resource('dynamodb')
slots_table = dynamodb.Table('Slots')
appointments_table = dynamodb.Table('Appointments')

# Hardcoded default values mapping to your database items perfectly
DEFAULT_SLOTS = [
    {"slot_id": "SLOT_0900", "time_label": "09:00 AM - 10:00 AM"},
    {"slot_id": "SLOT_1000", "time_label": "10:00 AM - 11:00 AM"},
    {"slot_id": "SLOT_1100", "time_label": "11:00 AM - 12:00 PM"}
]

def lambda_handler(event, context):
    try:
        # 1. Scan and delete all current slots
        slots_response = slots_table.scan()
        existing_slots = slots_response.get('Items', [])

        with slots_table.batch_writer() as batch:
            for slot in existing_slots:
                # FIXED: Matches your table's exact Partition Key name
                batch.delete_item(Key={'slot_id': slot['slot_id']})

        # 2. Re-insert default slots (PRESERVED & CORRECTED)
        with slots_table.batch_writer() as batch:
            for item in DEFAULT_SLOTS:
                # FIXED: Pushes your exact live schema attributes
                batch.put_item(Item={
                    'slot_id': item['slot_id'],
                    'time_label': item['time_label'],
                    'status': 'available'
                })

        # 3. Scan and delete all appointments
        appointments_response = appointments_table.scan()
        existing_appointments = appointments_response.get('Items', [])

        with appointments_table.batch_writer() as batch:
            for appointment in existing_appointments:
                # FIXED: Matches your table's exact Partition Key name
                batch.delete_item(Key={'appointment_id': appointment['appointment_id']})

        return {
            'statusCode': 200,
            'body': 'Slots and appointments reset successfully.'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
