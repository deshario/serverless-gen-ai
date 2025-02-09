import json
import boto3

ses_client = boto3.client("ses", region_name="ap-southeast-1")

def handler(event, context):
    try:
        summary_text = event.get("SummaryText", "No summary provided.")
        doctor_email = event.get("DoctorEmail", "") 

        subject = "Appointment Request: Urgent Medical Consultation Required"
        body = f"""
        Dear Doctor,

        A patient requires an urgent medical consultation based on their recent blood test analysis.  
        The system has detected a **Critical** condition, and immediate attention is needed.

        **Patient Report Summary:**
        {summary_text}

        Please proceed with scheduling an appointment at the earliest convenience.  
        Kindly confirm availability for the consultation.

        Best Regards,  
        Medical Report Automation System
        """

        response = ses_client.send_email(
            Source='deshario9@gmail.com',
            Destination={"ToAddresses": [doctor_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            },
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Appointment request email sent successfully!", "response": response}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
