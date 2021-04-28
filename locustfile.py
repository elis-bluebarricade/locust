import os

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from locust import task, TaskSet, HttpUser
from locust.contrib.fasthttp import FastHttpUser

import greenlet
import logging, sys

import json
from json import JSONDecodeError

# Environment Variables
#
# BB_API_KEY
#    this needs to be set for this demo locustfile
#
# LOCUST_WORKER_ID (NOT USED)
#    set this on the client, dictates the blockchain address range used 
#

# https://blockchain-api-blockchain-project.apps.ocp1.ocp.hcl.local/greenbay-network

# try:
#     LOCUST_WORKER_ID = os.environ['LOCUST_WORKER_ID']
# except KeyError:
#     LOCUST_WORKER_ID = 0 # default to first worker address range

try:
    BB_API_KEY = os.environ['BB_API_KEY']
except KeyError:
    BB_API_KEY = "" # Error, this needs to be set as environment variable

#   index   sender  receiver
#   0       0       1
#   1       2       3
#   2       4       5
#   3       6       7
#   4       8       9
#   5       10      11
#   ...     ...     ...

#def get_ids(index):
#    sender = index*2
#    receiver = index*2+1

# def get_addresses(index):
#     sender_addr = "worker_{}_addr_{}".format(LOCUST_WORKER_ID, index*2)
#     receiver_addr = "worker_{}_addr_{}".format(LOCUST_WORKER_ID, index*2+1)
#     return (sender_addr, receiver_addr)

class BlueBarricadeUser(FastHttpUser):

    # user_id = -1
    # sender_addr = ""
    # receiver_addr = ""

    #def on_start(self):
        # print("user {} started.\n".format(greenlet.getcurrent().minimal_ident))
        # self.user_id = greenlet.getcurrent().minimal_ident
        # self.sender_addr, self.receiver_addr = get_addresses(self.user_id)
        # self.sender_addr = self.user_id
        # self.receiver_addr = self.user_id
        # print("\n\n{} : {}, {}".format(self.user_id, self.sender_addr, self.receiver_addr))

    @task
    def transfer(self):
        with self.client.post("/transferMoneyExperimental", verify=False, catch_response=True,
            headers={"API_KEY" : BB_API_KEY},
            json={
                "senderAddress": "experimental_senderAddress",
                "receiverAddress": "experimental_receiverAddress",
                "sendAmount": 1,
                "receiveAmount": 0.8
            },
        ) as response:
            try:
                # print("HTTP status: " + str(response.status_code))
                if response.status_code != 200:
                    response.failure("Response Error: HTTP status: " + str(response.status_code))
                else:
                    jsonResponse = response.json()
                    if jsonResponse["success"] == True:
                        if jsonResponse["result"]["txId"]:
                            # print("OK, Got txId: " + jsonResponse["result"]["txId"])
                            response.success()
                        else:
                            response.failure("Response Error: Success but no txid: " + response.text)
                    else:
                        message = jsonResponse["message"]
                        try:
                            jsonMessage = json.loads(message)
                            response.failure("Response Error (success==false) inner message: " + jsonMessage["message"])
                        except:
                            response.failure("Response Error (success==false) message: " + message)
            except JSONDecodeError:
                response.failure("Response Error (JSONDecodeError) : " + response.text)
            except:
                response.failure("Response Error (exception): " + response.text)
