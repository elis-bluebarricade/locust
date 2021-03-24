import os

import random
from locust import HttpUser, task, between

# use this URL for this demo
# url https://blockchain-api-blockchain-project.apps.ocp1.ocp.hcl.local/greenbay-channel

# Environment Variables
#
# GREENBAY_API_KEY
#    this needs to be set for this demo locustfile
#

try:
    GREENBAY_API_KEY = os.environment['GREENBAY_API_KEY']
except KeyError:
    GREENBAY_API_KEY = "" # Error, this needs to be set as environment variable

class TestPoC2(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def getTransactionInfo(self):
        self.client.post("/getTransactionInfo", verify=False,
            headers={"API_KEY" : GREENBAY_API_KEY},
            json={"txId": "ef759d6bd85f9a5ffd5c20ac83ad177372002f3cf3b8e916a4a39c6a73b66595"},
        )

    @task
    def getAddressInfo(self):
        for i in range(10):
            self.client.post("/getAddressInfo", verify=False, 
                headers={"API_KEY" : GREENBAY_API_KEY},
                json={"address": "test_address_" + str(random.randint(1, 99))	},
            )

    @task
    def listTransaction(self):
        self.client.post("/listTransaction", verify=False,
            headers={"API_KEY" : api_key},
            json={    
                "pageSize": 10,
                "bookMark": "",
                "eventType": "all" 
            },
        )
