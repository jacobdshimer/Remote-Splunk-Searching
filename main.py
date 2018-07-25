import authenticate as auth
import search

hostname = ""
username = ""
password = ""
splunkdPort = ""
searchString = ""
sessionKey = auth.getLogon(hostname,username,password,splunkdPort)
srch = search.sendSearch(sessionKey,hostname,splunkdPort,searchString)
