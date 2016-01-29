__author__ = 'Assaf Dekel'


import requests, json
import ParseAPI as parse
from simple_salesforce import Salesforce
import gglAdwordsLogin as adWordsLogin
import gglPushEmails as adWordsEmails
import fbPushEmails as fbEmails

"""
# OAuth 2.0 credential information. In a real application, you'd probably be
# pulling these values from a credential storage.
CLIENT_ID - of developer account
CLIENT_SECRET - of developer account
REFRESH_TOKEN - put access token!! of user account. from Parse.com

# AdWords API information.
DEVELOPER_TOKEN - of developer's account
USER_AGENT = '3Targeting'
CLIENT_CUSTOMER_ID - the number of the user's googleAds account
"""
# Developer's keys
# OAuth 2.0 credential information
CLIENT_ID = '280160838890-kjhls6qlss26fj1f2kr7v61fh5esmmuk.apps.googleusercontent.com'
CLIENT_SECRET = 'ZQLzF8TadPS3Zpk52rACGsKG'

# AdWords API information.
DEVELOPER_TOKEN = 'YAVzDP8OR2vtzQ_Bp_ztFA'
USER_AGENT = '3Targeting'

# SHOULD BE SUPPLIED BY YANIR!!!
test_CLIENT_CUSTOMER_ID = '543-963-1369'
production_CLIENT_CUSTOMER_ID = '393-270-7738'


def getLeadsList(sf):

    try:
        response = sf.query_all("SELECT Email FROM Lead WHERE Email <> ''")
    except Exception, e:
        if e.status == 401:
            SALESFORCE_REFRESH_URL = "https://login.salesforce.com/services/oauth2/token"
            SALESFORCE_CONSUMER_KEY = "3MVG98_Psg5cppyYH7Cios03svOf9hpZtPg.n0yTXRIKlnjy43.MNRgdLDbmBc3T5wK2IoYOaPLNlqBzNouzE"
            SALESFORCE_CONSUMER_SECRET = "2132402812325087889"

            # HTTP request
            url = SALESFORCE_REFRESH_URL
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + salesforce_access_token,
                'X-PrettyPrint': '1'
            }
            params = {'grant_type': 'refresh_token',
                      'client_id': SALESFORCE_CONSUMER_KEY,
                      'client_secret': SALESFORCE_CONSUMER_SECRET,
                      'refresh_token': salesforce_refresh_token }
            result = requests.get(url, headers=headers, params=params)

            newSfCred = json.loads(result.content)
            sfCred['instance_url'] = newSfCred['instance_url']
            sfCred['access_token'] = newSfCred['access_token']
            sfCred['signature'] = newSfCred['signature']
            sfCred['id'] = newSfCred['id']
            sfCred['issued_at'] = newSfCred['issued_at']
            parse.pushSalesforceCredentials(user_account,sfCred)

            # try with new token
            sf = Salesforce(instance_url=sfCred['instance_url'], session_id=sfCred['access_token'])
            response = sf.query_all("SELECT Email FROM Lead WHERE Email <> ''")
    return response

def pushAdwordsCredentialsIfChanged(adwords_access_token, new_adwords_access_token, adwords_refresh_token, new_adwords_refresh_token):
    if new_adwords_access_token != adwords_access_token:
        adwords_access_token = new_adwords_access_token
    if new_adwords_refresh_token != adwords_refresh_token:
        adwords_refresh_token = new_adwords_refresh_token
    parse.pushAdwordsCredentials(user_account, new_adwords_access_token, new_adwords_refresh_token)

"""
V Register to parse
  Get all active users from Parse
for each user:
V Get SF credentials
V Login to SF
V Get leads list
V Convert to emailsList
V Convert to google AdWords format

--- AdWords ---
V Login to AdWords
V Send to google AdWords
--- Facebook ---
 Login to Facebook
 Get custom audiences
 Send to Facebook (to specific custom audience)


"""
user_account = "V5BwqwF0Es"

#get instance_url & Access_token from Parse.com
# session_id='' == Access Token
"""
___________________ Parse ___________________
"""
# Register to parse
parse.register2remoteDB()

# Get SF credentials
sfCred = parse.getSalesforceCredentials(user_account)
salesforce_instance_url = sfCred['instance_url']
salesforce_access_token = sfCred['access_token']
salesforce_refresh_token = sfCred['refresh_token']

"""
______________________ Salesforce ______________________
"""
# Login to SF
sf = Salesforce(instance_url=salesforce_instance_url, session_id=salesforce_access_token)

#import pytz
#import datetime
#end = datetime.datetime.now(pytz.UTC) # we need to use UTC as salesforce API requires this
#sf.Contact.updated(end - datetime.timedelta(days=10), end)

# Get leads list
leadsList = getLeadsList(sf)

"""
_________________ Prepare Emails List _________________
lowercase & hash
"""

# Convert to emailsList
emailsList =[]
#emailsList = leadsList['records'][i]['Email']
for lead in leadsList['records']:
    emailsList.append(lead['Email'])

# Normalize & Hash emails
hashedEmails = adWordsEmails.HashEmails(emailsList)

"""
_________________ AdWords _________________
"""

# # get adWords credentials
# adwordsCred = parse.getAdwordsCredentials(user_account)
# adwords_access_token = adwordsCred['access_token']
# adwords_refresh_token = adwordsCred['refresh_token']
#
# # SHOULD BE SUPPLIED BY YANIR!!!
# CLIENT_CUSTOMER_ID = test_CLIENT_CUSTOMER_ID
#
# # Login to AdWords
# # if can't connect with REFRESH_TOKEN try to connect with ACCESS_TOKEN !! it worked!
# [adwordsClient, new_adwords_access_token, new_adwords_refresh_token] = adWordsLogin.login(CLIENT_ID, CLIENT_SECRET, adwords_refresh_token, DEVELOPER_TOKEN, USER_AGENT, CLIENT_CUSTOMER_ID)
#
# # Upload emails list to adwords
# adWordsEmails.sendHashedEmails(adwordsClient, hashedEmails)
#
# # Push new credentials to Parse
# pushAdwordsCredentialsIfChanged(adwords_access_token, new_adwords_access_token, adwords_refresh_token, new_adwords_refresh_token)
#
# print "Success"

"""
_________________ Facebook _________________
"""
# get fb credentials
fbCred = parse.getFacebookCredentials(user_account)
fb_access_token = fbCred['user_token']['accessToken']
# fb push emails
retVal = fbEmails.facebookMain(fbCred, emailsList)
#sendHashedEmails(emailsList, hashedEmails)
print retVal
