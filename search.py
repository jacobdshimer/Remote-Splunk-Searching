def sendSearch(sessionKey,hostname,splunkdPort,searchQuery):
    import requests
    import json
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    url = "https://" + str(hostname) + ":" + str(splunkdPort) + \
          "/services/search/jobs"
    querystring = {"output_mode":"json"}
    payload = 'search=search ' + str(searchQuery)
    headers = {
        'Authorization': 'Splunk ' + str(sessionKey),
        'Content-Type': "application/x-www-form-urlencoded"
        }

    response = requests.request("POST", url, data=payload, headers=headers, \
                                params=querystring, verify=False)
    parsed_json = json.loads(response.text)
    print(parsed_json['sid'])

#def checkSearchStatus(sessionKey,sid):
