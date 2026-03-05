from pathlib import Path
import argparse

def readJson(filename):
    data = {}
    with open(filename, "r") as f:
        content = f.read().strip()
        if content.startswith("{") and content.endswith("}"):
            content = content[1:-1].strip()
        if content:
            pairs = content.split(",")
            for pair in pairs:
                key, value = pair.split(":")
                key = key.strip().strip('"')
                value = value.strip().strip('"')
                data[key] = value
    return data

def writeJson(filename, data):
    with open(filename, "w") as f:
        f.write("{\n")
        for i, (key, value) in enumerate(data.items()):
            line = f'  "{key}": "{value}"'
            if i < len(data) - 1:
                line += ","
            line += "\n"
            f.write(line)
        f.write("}\n")

def readYaml(filename):
    data = {}
    with open(filename, "r") as f:
        current_key = None
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ": " in line:
                key, value = line.split(": ", 1)
                key = key.strip()
                value = value.strip()
                if value == "":
                    data[key] = []
                    current_key = key
                else:
                    data[key] = value
                    current_key = None
            elif line.startswith("- ") and current_key:
                item = line[2:].strip()
                data[current_key].append(item)
    return data

def writeYaml(filename, data):
    with open(filename, "w") as f:
        for key, value in data.items():
            if isinstance(value, list):
                f.write(f"{key}:\n")
                for item in value:
                    f.write(f"  - {item}\n")
            else:
                f.write(f"{key}: {value}\n")

parser = argparse.ArgumentParser(description="Json/YAML reader and writer to files")
parser.add_argument("-rf", "--readfile", help="JSON/YAML file to read logs from", type=str, required=True)
parser.add_argument("-wf", "--writefile", help="File name to write logs to", type=str, required=True)
args = parser.parse_args()

readFilePath = Path(args.readfile)

if not (readFilePath.exists() and readFilePath.is_file()):
    print("Specified read file does not exist!")
    exit(1)

if readFilePath.suffix == ".json":
    try:
        data = readJson(args.readfile)
        writeJson(args.writefile, data)
        print("JSON logs written to file")
    except Exception as e:
        print("Error processing file:", e)
elif readFilePath.suffix in (".yaml", ".yml"):
    try:
        data = readYaml(args.readfile)
        writeYaml(args.writefile, data)
        print("YAML logs written to file")
    except Exception as e:
        print("Error processing file:", e)
else:
    print("Unsupported file type!")