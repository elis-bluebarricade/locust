import os

# Environment Variables
#
# LOCUST_SETTING
#    set this to "master" or "worker", or leave blank for default (single node, no workers)
#
# LOCUST_MASTER_PORT
#    set this for the worker, leave blank for default 5557
#

try:
    LOCUST_SETTING = os.environ['LOCUST_SETTING']
except KeyError:
    LOCUST_SETTING = "default"

#try:
#    LOCUST_MASTER_PORT = os.environ['LOCUST_MASTER_PORT']
#except KeyError:
#    LOCUST_MASTER_PORT = 5557

os.system("python setup.py build")
os.system("python setup.py install")

if LOCUST_SETTING.lower() == "master":
    os.system("locust -f locustfile.py --master --web-port 8080")
elif LOCUST_SETTING.lower() == "slave" or LOCUST_SETTING.lower() == "worker":
    os.system("locust -f locustfile.py --worker)
    #os.system("locust -f locustfile.py --worker --master-port={}".format(LOCUST_MASTER_PORT))
else:
    os.system("locust -f locustfile.py --web-port 8080")
