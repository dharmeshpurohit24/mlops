## AWS Pipeline

## Working Flow
1. Upload a ZIP file to input S3 bucket(itt-assignmnet-input)
2. S3 triggers Lambda (s3-put-event) to take file name and send to SNS and SQS
4. Lambda (s3-sqs-worker) reads from SQS
5. ZIP is downloaded and extracted (file inside zip)
6. .txt / .json files are converted to CSV (using inbuilt csv)
7. The CSV files are uploaded to output S3 bucket(itt-assignment-output)
