import json
import os
from utils.s3_helper import download_zip, upload_csv
from utils.file_processor import extract_zip, convert_files_to_csv

INPUT_BUCKET = 'itt-assignmnet-input'
OUTPUT_BUCKET = 'itt-assignment-output'

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            file_name = body['file_name']
        except (json.JSONDecodeError, KeyError):
            print("Invalid SQS message:", record['body'])
            continue

        print(f"Processing file: {file_name}")

        local_zip = f"/tmp/{os.path.basename(file_name)}"
        extract_dir = "/tmp/extracted"
        os.makedirs(extract_dir, exist_ok=True)

        # Download zip
        download_zip(INPUT_BUCKET, file_name, local_zip)

        # Extract zip
        extract_zip(local_zip, extract_dir)

        # Convert and upload
        convert_files_to_csv(
            extract_dir,
            OUTPUT_BUCKET,
            lambda key, path: upload_csv(OUTPUT_BUCKET, key, path)
        )

        print(f"Finished processing: {file_name}")
