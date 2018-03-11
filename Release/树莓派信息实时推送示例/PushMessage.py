# Author:YinChao
# Date:2017-12-21
# ver:V0.1

import pycurl,json

def push(str):
    appID = "59edd424a4c48aee80d6dd4a"
    appSecret = "05cc2a44d97e361f14d28c0ab8ff4acd"
    pushEvent = "DoorAlert"
    pushMessage = str

    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.instapush.im/v1/post')
    c.setopt(c.HTTPHEADER,['x-instapush-appid:' + appID,'x-instapush-appsecret:' + appSecret, 'Content-Type:application/json'])

    json_fields = {}
    json_fields['event'] = pushEvent
    json_fields['trackers'] = {}
    json_fields['trackers']['message'] = pushMessage

    postfields = json.dumps(json_fields)

    c.setopt(c.POSTFIELDS, postfields)

    c.perform()

    c.close()



