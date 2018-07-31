
def getLogon(hostname,username,password,splunkdPort):
    import requests
    import json
    #This is to get rid of the problem of splunk running their own SSL certs for splunkd
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    url = "https://" + str(hostname) + ":" + str(splunkdPort) + \
          "/services/auth/login/"
    querystring = {"output_mode":"json"}
    payload = "username=" + str(username) + "&password=" + str(password)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
    #Post the request to the splunkd /services/auth/login endpoint to get a session key
    #This is so that the user isn't constantly sending their credentials across the wire
    #Future plans looking into securing this
    response = requests.request("POST", url, data=payload, headers=headers, \
                                params=querystring, verify=False)
    results = (response.text)
    if 'message' in results:
        results = json.loads(results)
        return results['messages'][0]['type'] + ": " + results['messages'][0]['text']
    else:
        results = json.loads(results)
        return results['sessionKey']

def deleteSession(sessionKey,hostname,splunkdPort):
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    url = "https://" + str(hostname) + ":" + str(splunkdPort) + "/services/authentication/httpauth-tokens/" + str(sessionKey)

    headers = {
        'Authorization': "Splunk " + str(sessionKey),
        'Cache-Control': "no-cache",
        }

    response = requests.request("DELETE", url, headers=headers)

#This is so that the user can authenticate using an interactive prompt
#don't know how useful this is currently, but eh its there
if __name__ == "__main__":
    url = input("What is the name of the server? ")
    username = input("What is the username? ")
    password = input("What is the password? ")
    sessionKey = getLogon(url,username,password)
    print(sessionKey)
