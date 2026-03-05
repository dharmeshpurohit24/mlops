from pathlib import Path
import argparse
import json
import yaml

parser = argparse.ArgumentParser(description="Reads the json/yaml from file and write logs to file specified")
parser.add_argument("-rf", "--readfile", help="json/yaml file to read the logs from", type=str, required=True)
parser.add_argument("-wf", "--writefile", help="File name where the logs are to be written", type=str, required=True)

args = parser.parse_args()

readFilePath = Path(args.readfile)

if not (readFilePath.exists() and readFilePath.is_file()):
    print("Specified read file does not exist!")
    exit(1)

if readFilePath.suffix == ".json":
    try:
        with open(args.readfile, "r") as rf:
            data = json.load(rf)

            with open(args.writefile,"w") as wf:
                wf.write(json.dumps(data,indent=2))
        print("Json logs written to file")

    except json.JSONDecodeError: 
        print("Json is invalid !")
    
elif readFilePath.suffix in (".yaml",".yml"):
    try:
        with open(args.readfile, "r") as rf:
            data = yaml.safe_load(rf)

            with open(args.writefile,"w") as wf:
                wf.write(yaml.safe_dump(data))
        print("Yaml logs written to file")

    except yaml.YAMLError: 
        print("Yaml is invalid !")

else: 
    print("Wrong file type !")