__author__ = 'assafdekel'

import urllib2, json

class MktoCredentials():
   def __init__(self):
       self.munchkin = None
       self.clientId = None
       self.clientSecret = None


#Client Application will make a GET request to the Identity service
# In: user credentials
# Out: Access Token
def getToken(munchkinID, customServiceClientId, customServiceClientSecret):
    identityServiceURL = "https://%s.mktorest.com/identity" % munchkinID
    tokenURL = "%s/oauth/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (identityServiceURL, customServiceClientId, customServiceClientSecret)
    mktoResponse = urllib2.urlopen(tokenURL)
    jsonToken = json.load(mktoResponse)
    accessToken = jsonToken["access_token"]
    return accessToken;

    """
    jsonToken json structure
    Note: expires_in is returned in seconds

    {
        "access_token": "cdf01657-110d-4155-99a7-f986b2ff13a0:int",
        "token_type": "bearer",
        "expires_in": 3599,
        "scope": "apis@acmeinc.com"
    }
    """

def buildMktoQueryURL(munchkinID, accessToken, fields):
    mktoQueryURL = "https://%s.mktorest.com/rest/v1/leads.json?access_token=%s&filterType=id&filterValues=1,2,3,4,5,6,7,8,9,10,11,12,13&fields=%s&batchSize=100&_method=GET" % (munchkinID, accessToken, fields)
    return mktoQueryURL

# In: Access Token
# Out: Mkto response (should be leeds - JSON)
def queryMkto(munchkinID, accessToken, fields):
    mktoQueryURL = buildMktoQueryURL(munchkinID, accessToken, fields)
    mktoResponse = urllib2.urlopen(mktoQueryURL)
    mktoResponseJson = json.load(mktoResponse)
    return mktoResponseJson

# In: Leeds in JSON format
# Out: True = Valid, False = Access Token timed out / bad response
def isValidResponse(mktoResponseJson):
    try:
        valid = mktoResponseJson['success']
        return valid;
    except:
        return False;