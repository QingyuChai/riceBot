import json
import sys
import subprocess
import pycurl

#str_replace("<break/>")
class send_fb:
    def __init__(self):
        self.receiver = "1870357256323127"
        self.token = "EAASEeFpPvkABAJ9676sXYE1E8qeM7qOCCuuLkZB9lkYABmZCZAyZAk7ZA6WHZBQlGNY0PlPGJOtcd81xv4ON2bhOeWMZBuUYRTP7ZCMq2K2jVDvZB0GhktwaQZCGldFSlN5udOYRY4pNEf6OdfwZCe6QvNL5uCwYMOcMTPgApkhv8Mx5gZDZD"

    def message_validate(self, message):
        to_return = {
                        "recipient" : {
                            "id" : self.receiver
                        },
                        "message" : {
                            "text" : message
                        }
                    }
        return to_return


    def send(self, message):
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(self.token)
        #get what should be run
        #loop and check if message is list
        to_reply = json.dumps(self.message_validate(message))

        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.POSTFIELDS, to_reply)
        c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])

        c.perform()
