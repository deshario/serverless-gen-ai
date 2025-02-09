import os
import boto3
import json
from datetime import datetime

s3 = boto3.client('s3')

def handler(event, context):
    try:
        summary_text = event.get('SummaryText', '')
        output_bucket = event.get('OutputBucket', '')
        file_name = event.get('FileName', '')

        if not summary_text or not output_bucket or not file_name:
            raise ValueError("Missing required input parameters: SummaryText, OutputBucket, or FileName")

        base_file_name = os.path.splitext(file_name)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        s3_key = f"report_highlights/{base_file_name}_{timestamp}.txt"

        # Save the processed report to S3
        s3.put_object(
            Bucket=output_bucket,
            Key=s3_key,
            Body=summary_text,
            ContentType='text/plain'
        )

        s3_location = f"s3://{output_bucket}/{s3_key}"
        print(f"Report saved to {s3_location}")

        return {
            "S3Location": s3_location
        }
    except Exception as e:
        print(f"Error saving report to S3: {e}")
        raise e