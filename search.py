def sendSearch(sessionKey,hostname,splunkdPort,searchQuery):
    import requests
    import json
    import time
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
    return parsed_json['sid']

def checkSearchStatus(sessionKey,hostname,splunkdPort,sid):
    import requests
    import json
    from time import sleep
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    while True:
        url = "https://" + str(hostname) + ":" + str(splunkdPort) + \
              "/services/search/jobs/" + str(sid) + "/"
        querystring = {"output_mode":"json"}
        headers = {
            'Authorization': 'Splunk ' + str(sessionKey),
            'Content-Type': "application/x-www-form-urlencoded"
            }

        response = requests.request("GET", url, headers=headers, \
                                    params=querystring, verify=False)

        parsed_json = json.loads(response.text)
        if (parsed_json['entry'][0]['content']['isDone']) == True and (parsed_json['entry'][0]['content']['isFailed']) == False:
            status = "Your search is done, grabbing the results.  It finished in " + str(parsed_json['entry'][0]['content']['runDuration'])
            break

        elif (parsed_json['entry'][0]['content']['isDone']) == True and (parsed_json['entry'][0]['content']['isFailed']) == True:
            status = str(parsed_json['entry'][0]['content']['messages'][0]['type']) + ": " + str(parsed_json['entry'][0]['content']['messages'][0]['text'])
            break

        sleep(2)

    return status
