
def getLogon(url,username,password):
    import requests
    querystring = {"output_mode":"json"}
    payload = "username=" + str(username) + "&password=" + str(password)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers, \
                                params=querystring, verify=False)

    sessionKey = response.text.split(":")[1].strip('"').strip('"}')
    return sessionKey

if __name__ == "__main__":
    url = input("What is the URL? ")
    username = input("What is the username? ")
    password = input("What is the password? ")
    sessionKey = getLogon(url,username,password)
    print(sessionKey)
