import argparse
from datetime import datetime
import sys

parser = argparse.ArgumentParser(description="script to check if env is passed")
parser.add_argument("--env",choices=["dev","stage","prod"])
parser.add_argument("--verbose",action="store_true")

args = parser.parse_args()
date_time = datetime.now()

if not args.env:
    exit(1)

if args.verbose:
    print("Hello from", args.env, "!")
    print("Environment validated successfully")
    print("Script executed at", date_time.strftime("%Y-%m-%d %H:%M:%S"))
    print("Python version:",sys.version.split()[0])
else:
    print("Hello from", args.env, "!")