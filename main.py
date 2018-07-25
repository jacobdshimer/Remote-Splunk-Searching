import authenticate as auth
import search

hostname = "ds37812-14.class.splunk.com"
sessionKey = auth.getLogon(hostname,"admin","splunk","8089")
srch = search.sendSearch(sessionKey,hostname,"8089","index=_internal | top stats host")
