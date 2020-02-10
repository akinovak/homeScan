import os
import time
from datetime import datetime
while True:
    start_time = datetime.now()
    os.system('python3 crawl_process.py')
    os.system('python3 delete_script.py polovni')
    end_time = datetime.now()
    diff = int((end_time - start_time).total_seconds())
    sleep_time = 24*60*60 - diff
    time.sleep(sleep_time)
