from urllib.request import urlopen
import json
token2 = '4227a26ce4566cb71e2e4128216bc855b2fd98f2c5f5014a5f3ecec5920c35807ff9c6bb98efbde00f7fd'
token = 'f9d0e57344335338822264ac30ced3787880e307cb401c9d0ac05ce9cc28de27b4b2183b850dfad2d6d38'
address = 'https://api.vk.com/method/audio.get?owner_id={}&access_token={}&v=5.92'.format('536997',token2)
data = urlopen(address)
decoded_response = data.read().decode()
final_data = json.loads(decoded_response)
print(final_data)