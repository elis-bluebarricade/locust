import os

# Environment Variables
#
# LOCUST_SETTING
#    set this to "master" or "worker", or leave blank for default (single node, no workers)
#
# LOCUST_HOST_IP
#    set this on the worker node, IP of the master node
#

try:
    LOCUST_SETTING = os.environ['LOCUST_SETTING']
except KeyError:
    LOCUST_SETTING = "default"

try:
    LOCUST_HOST_IP = os.environ['LOCUST_HOST_IP']
except KeyError:
    LOCUST_HOST_IP = "localhost"
    
os.system("python setup.py build")
os.system("python setup.py install")

if LOCUST_SETTING.lower() == "master":
    os.system("locust -f locustfile.py --master --web-port 8080")
elif LOCUST_SETTING.lower() == "slave" or LOCUST_SETTING.lower() == "worker":
    os.system("locust -f locustfile.py --worker --master-host={}".format(LOCUST_HOST_IP))
else:
    os.system("locust -f locustfile.py --web-port 8080")
