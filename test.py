import apiai
import codecs
import json
CLIENT_ACCESS_TOKEN = '289a95d5bc84431bb1f6b6a10100e805'
AI = apiai.ApiAI(client_access_token=CLIENT_ACCESS_TOKEN)
request = AI.text_request()
request.lang = 'russian'
request.session_id = '<SESSION ID, UNIQUE FOR EACH USER>'
for _ in range(10):
    request.query = input()
    response = request.getresponse()
    reader = codecs.getdecoder('utf-8')
    obj = json.loads(response.read())
    reply = obj['result']['fulfillment']['speech']
    print(reply)