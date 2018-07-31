def sendSearch(sessionKey,hostname,splunkdPort,searchQuery):
    import requests
    import json
    import time
    #This is to get rid of the problem of splunk running their own SSL certs for splunkd
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    #Crafting the packet to /services/search/jobs
    url = "https://" + str(hostname) + ":" + str(splunkdPort) + "/services/search/jobs"
    #Turns the output into json format
    querystring = {"output_mode":"json"}
    payload = 'search=search ' + str(searchQuery)
    headers = {
        'Authorization': 'Splunk ' + str(sessionKey),
        'Content-Type': "application/x-www-form-urlencoded"
        }

    #Post the request to splunkd.  Verifiy was turned off for the same reason
    #we're ignoring the warning up above, splunkd runs with its own certs and
    #can't be verified.  Might look at a more elegant solution in the future.
    response = requests.request("POST", url, data=payload, headers=headers, \
                                params=querystring, verify=False)
    #gets the response and loads it into parsed_json
    parsed_json = json.loads(response.text)
    return parsed_json['sid']

def checkSearchStatus(sessionKey,hostname,splunkdPort,sid):
    import requests
    import json
    from time import sleep
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    #while True loop to send the request back to splunkd asking if it finished
    #the program was executing faster then splunkd could process the search so had
    #to do this and add the wait time at the end.
    while True:
        url = "https://" + str(hostname) + ":" + str(splunkdPort) + "/services/search/jobs/" + str(sid) + "/"
        querystring = {"output_mode":"json"}
        headers = {
            'Authorization': 'Splunk ' + str(sessionKey),
            'Content-Type': "application/x-www-form-urlencoded"
            }

        #get the status of the search by querrying /services/search/sid/jobs/
        response = requests.request("GET", url, headers=headers, params=querystring, verify=False)

        parsed_json = json.loads(response.text)
        #If the isDone key returns True and the isFailed key returns False, save the status
        #and break out of the loop
        status = []
        if (parsed_json['entry'][0]['content']['isDone']) == True and (parsed_json['entry'][0]['content']['isFailed']) == False:
            status.append("Your search is done, grabbing the results.  It finished in " + str(parsed_json['entry'][0]['content']['runDuration']))
            status.append(True)
            break
        #If the isDone key returns True and the isFailed key returns True, save the status
        #explaining the problem and break out of the loop
        elif (parsed_json['entry'][0]['content']['isDone']) == True and (parsed_json['entry'][0]['content']['isFailed']) == True:
            status.append(str(parsed_json['entry'][0]['content']['messages'][0]['type']) + ": " + str(parsed_json['entry'][0]['content']['messages'][0]['text']))
            status.append(False)
            break

        sleep(2)

    return status

def getResults(sessionKey,hostname,splunkdPort,sid,output_mode):
    import requests
    import json
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    url = "https://" + str(hostname) + ":" + str(splunkdPort) + "/services/search/jobs/" + str(sid) + "/results/"
    querystring = {"output_mode":output_mode,"count":"0"}
    headers = {
        'Authorization': 'Splunk ' + str(sessionKey),
        'Content-Type': "application/x-www-form-urlencoded"
        }
    response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
    return response.text
