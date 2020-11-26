import requests
import json

URL = 'http://121.170.193.221:53004/shell-list'
data = {"svr":"121.170.193.200","db":"IBRM","usePath":"Y","path":"/u01/SCRIPTS/Database/IBRM/RMAN"}
#
# res = requests.post(URL, data=data)
#
# print res




data = json.dumps(data)

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
res = requests.post(URL, params={'result':data}, verify=False , headers=headers)

print(res.text)
print(res.status_code)