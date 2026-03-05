# import library
import schedule
import time
from time_checker.core import check_assignment

schedule.every(30).seconds.do(check_assignment)

while True:
    schedule.run_pending()
    time.sleep(1)
