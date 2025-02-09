import boto3
import os
import json

textract = boto3.client('textract')
# s3 = boto3.client('s3')

def handler(event, context):
    try:
        # Extract input parameters
        job_id = event['JobId']
        output_bucket = event['OutputBucket']
        file_name = event['FileName']

        if not job_id or not output_bucket or not file_name:
            raise ValueError("Missing required input parameters: JobId, OutputBucket, or FileName")

        # Fetch Textract results
        textract_response = textract.get_document_text_detection(JobId=job_id)

        # Extract text from the Textract response
        extracted_text = ""
        for block in textract_response.get('Blocks', []):
            if block['BlockType'] == 'LINE':  # Filter for LINE blocks
                extracted_text += block.get('Text', '') + "\n"

        # Check if extracted text is empty
        if not extracted_text.strip():
            raise Exception("No text was extracted from the document.")

        # Remove the file extension from the file name
        # base_file_name = os.path.splitext(file_name)[0]  # Removes the extension

        # s3_key = f"results/{base_file_name}.txt"

        # s3.put_object(
        #     Bucket=output_bucket,
        #     Key=s3_key,
        #     Body=extracted_text,
        #     ContentType='text/plain'
        # )

        return {
            # "S3Location": f"s3://{output_bucket}/{s3_key}",
            "ExtractedText": extracted_text
        }
    except Exception as e:
        print(f"Error processing Textract results: {e}")
        raise e  # Ensure the Step Function knows if something fails