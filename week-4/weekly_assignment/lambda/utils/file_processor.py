import os
import zipfile
import json
import csv

def extract_zip(zip_path, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

def convert_files_to_csv(extract_dir, output_bucket, upload_func):
    for f in os.listdir(extract_dir):
        input_path = os.path.join(extract_dir, f)
        csv_path = f"/tmp/{os.path.splitext(f)[0]}.csv"

        if f.endswith('.txt'):
            with open(input_path, 'r') as infile, open(csv_path, 'w', newline='') as outfile:
                reader = csv.reader(infile, delimiter='\t')
                writer = csv.writer(outfile)
                for row in reader:
                    writer.writerow(row)

        elif f.endswith('.json'):
            with open(input_path, 'r') as infile, open(csv_path, 'w', newline='') as outfile:
                data = json.load(infile)
                if isinstance(data, list) and data:
                    writer = csv.DictWriter(outfile, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    writer = csv.writer(outfile)
                    writer.writerow(data.keys())
                    writer.writerow(data.values())
        else:
            continue

        upload_func(os.path.basename(csv_path), csv_path)
