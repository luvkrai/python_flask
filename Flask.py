from flask import Flask
import time
import subprocess
from concurrent.futures import ProcessPoolExecutor
import string
import random

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
# We can also use ThreadPoolExecutor here but its better to use ProcessPoolExecutor, we all know why
# NOTE: max_workers is the limit on the number of tasks your flask app can do at a given point of time,
# For example if we do
# for _ in range(10):
      # Run curl command
# Flask application will only run the number of tasks at a time based on the value of max_workers regardless of the number of requests coming through
executor = ProcessPoolExecutor(max_workers=2)

app = Flask(__name__)

@app.route('/')
def hello_world():
    #time.sleep(3)
    #p = subprocess.Popen("sleep 3",shell=True)
    #p.communicate()
    msg = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    executor.submit(some_long_task, msg, 10)
    return 'Task {} launched in background\n'.format(msg)

def some_long_task(msg,sleep_time):
    with open(msg, 'a') as the_file:
        the_file.write('Started the Job\n')
        for i in range(sleep_time):
            the_file.write(str(i)+"\n")
            time.sleep(1)
        the_file.write('Job done\n')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',threaded=True)