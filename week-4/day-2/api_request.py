import requests
import json
import argparse

testUrl = "https://jsonplaceholder.typicode.com/users"
defaultFileName = "reports.json"

def fetchData(url):
    try:
        resp = requests.get(url)

        if not (resp.ok):
            print("Cannot get the info of url\n")
            exit(1)

        return resp.json()

    except Exception as e:
        print("Cannot get from url")
        return []

def extractInfo(data):
    report = []

    for item in data:
        report.append({
            "id": item.get("id","undefined"),
            "name": item.get("name","undefined"),
            "email": item.get("email","undefined"),
            "city": item.get("address",{}).get("city","undefined"),
            "company": item.get("company",{}).get("name","undefined")
        })
        
    return report

parse = argparse.ArgumentParser(description="To write the report for a public api url")
parse.add_argument("-f","--filename",dest="inputFileName", help="File name to write the report in", default=defaultFileName)
args = parse.parse_args()

data = fetchData(testUrl)
report = extractInfo(data)
with open(args.inputFileName, "w") as fp:
    fp.write(json.dumps(report,indent=2))
    print(f"report generated and stored in file {args.inputFileName}")