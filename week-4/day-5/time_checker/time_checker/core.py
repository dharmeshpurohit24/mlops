from datetime import datetime

def check_assignment():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current date and time: {current_time}")
    print("Have you completed the assignment?")
