
def getLogon(hostname,username,password,splunkdPort):
    import requests
    import json
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    #url = "https://ds37812-14.class.splunk.com:8089/services/auth/login/"
    url = "https://" + str(hostname) + ":" + str(splunkdPort) + \
          "/services/auth/login/"
    querystring = {"output_mode":"json"}
    payload = "username=" + str(username) + "&password=" + str(password)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers, \
                                params=querystring, verify=False)

    sessionKey = json.loads(response.text)['sessionKey']
    return sessionKey

if __name__ == "__main__":
    url = input("What is the name of the server? ")
    username = input("What is the username? ")
    password = input("What is the password? ")
    sessionKey = getLogon(url,username,password)
    print(sessionKey)
