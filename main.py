import authenticate as auth
import search
import json

with open('settings.txt') as f:
    #settings = f.read()
    data = f.read()
    settings_json = json.loads(data)
print(settings_json)


searchString = "index=_internal | top host"
settings_json.update({'sessionKey':auth.getLogon(settings_json['hostname'],settings_json['username'],\
settings_json['password'],settings_json['splunkdPort'])})

settings_json.update({'sid':search.sendSearch(settings_json['sessionKey'],settings_json['hostname'],\
settings_json['splunkdPort'],searchString)})

status = search.checkSearchStatus(settings_json['sessionKey'],\
settings_json['hostname'],settings_json['splunkdPort'],settings_json['sid'])

print(settings_json)
print(status)
