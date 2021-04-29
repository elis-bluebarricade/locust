import os

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from locust import task, TaskSet, HttpUser, between
from locust.contrib.fasthttp import FastHttpUser

import greenlet
import logging, sys

import json
from json import JSONDecodeError

import time

# Environment Variables
#
# BB_API_KEY
#    this needs to be set for this demo locustfile
#

try:
    BB_API_KEY = os.environ['BB_API_KEY']
except KeyError:
    BB_API_KEY = "" # Error, this needs to be set as environment variable

class BlueBarricadeUser(FastHttpUser):
    wait_time = between(0, 0)

    #def on_start(self):
    #    print(self.host)

    @task
    def myTask(self):
        self.api_call = self.host.split('/')[-1]
        # print(self.api_call)
        if self.api_call == "transferMoneyExperimental":
            self.transfer()
        else:
            self.generic()
            #time.sleep(1)
    
    def transfer(self):
        with self.client.post("", verify=False, catch_response=True,
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

    def generic(self):
        with self.client.post("", verify=False, catch_response=True,
            headers={"API_KEY" : BB_API_KEY},
            json={
            },
        ) as response:
            if response.status_code != 200:
                response.failure("Response Error: HTTP status: " + str(response.status_code))
            else:
                response.success()
