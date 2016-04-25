__author__ = 'Assaf Dekel'

import requests, json
import mySQL
from simple_salesforce import Salesforce
import gglAdwordsLogin as adWordsLogin
import gglPushEmails as adWordsEmails
import fbPushEmails as fbEmails

LOG_FILE_NAME = "log.txt"

"""
# OAuth 2.0 credential information. In a real application, you'd probably be
# pulling these values from a credential storage.
CLIENT_ID - of developer account
CLIENT_SECRET - of developer account
REFRESH_TOKEN - put access token!! of user account. from db

# AdWords API information.
DEVELOPER_TOKEN - of developer's account
USER_AGENT = '3Targeting'
CLIENT_CUSTOMER_ID - the number of the user's googleAds account
"""
# Developer's keys
# OAuth 2.0 credential information
CLIENT_ID = '1021839565394-4pknihosad52tvejcaovp9mpnqtpm3qt.apps.googleusercontent.com'
CLIENT_SECRET = 'cCaORb7CqIWMeqZtsK6JTJsu'

# AdWords API information.
DEVELOPER_TOKEN = 'YAVzDP8OR2vtzQ_Bp_ztFA'
USER_AGENT = '3Targeting'

# SHOULD BE SUPPLIED BY YANIR!!!
test_CLIENT_CUSTOMER_ID = '543-963-1369'
production_CLIENT_CUSTOMER_ID = '393-270-7738'

def pushEmails2AdWords(hashedEmails,adwordsCred, db):
    adwords_access_token = adwordsCred['access_token']
    adwords_refresh_token = adwordsCred['refresh_token']

    # SHOULD BE SUPPLIED BY YANIR!!!
    CLIENT_CUSTOMER_ID = test_CLIENT_CUSTOMER_ID

    # Login to AdWords
    # if can't connect with REFRESH_TOKEN try to connect with ACCESS_TOKEN !! it worked!
    [adwordsClient, new_adwords_access_token, new_adwords_refresh_token] = adWordsLogin.login(CLIENT_ID, CLIENT_SECRET, adwords_refresh_token, DEVELOPER_TOKEN, USER_AGENT, CLIENT_CUSTOMER_ID)

    # Push new credentials to MySQL
    pushAdwordsCredentialsIfChanged(adwordsCred, new_adwords_access_token, new_adwords_refresh_token)

    # Upload emails list to adwords
    if adwordsCred['user_list_id'] != None:
        try:
            adWordsEmails.sendHashedEmails2ExistingList(adwordsClient,adwordsCred['user_list_id'], hashedEmails)
            return
        except Exception as e:
            if e.fault.detail.ApiExceptionFault.errors.reason == "INVALID_ID":
                print "No list with id: " + adwordsCred['user_list_id'] + "\nCreating new list..."

        user_list_id = adWordsEmails.sendHashedEmails(adwordsClient, hashedEmails)
        adwordsCred['user_list_id'] = user_list_id
        db.pushAdwordsCredentials(adwordsCred)
        print "New list created"
    return

def pushEmails2Facebook(hashedEmails,fbCred):

    #fb_access_token = fbCred['user_token']['accessToken']
    # fb push emails
    retVal = fbEmails.facebookMain(fbCred, emailsList)
    #sendHashedEmails(emailsList, hashedEmails)
    print retVal

# NOT OPERATIONAL!!
def pushEmails2Twitter(hashedEmails,twCred):

    from twitter_ads.client import Client
    from twitter_ads.audience import TailoredAudience
    from twitter_ads.enum import TA_LIST_TYPES, TA_OPERATIONS

    CONSUMER_KEY = 'your consumer key'
    CONSUMER_SECRET = 'your consumer secret'
    ACCESS_TOKEN = 'access token'
    ACCESS_TOKEN_SECRET = 'access token secret'
    ACCOUNT_ID = 'account id'

    # initialize the client
    client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # load the advertiser account instance
    account = client.accounts(ACCOUNT_ID)

    # create a new tailored audience
    audience = TailoredAudience.create(account, '/path/to/file', 'my list', TA_LIST_TYPES.EMAIL)

    # check the processing status
    audience.status()

    # update the tailored audience
    audience.update('/path/to/file', TA_LIST_TYPES.TWITTER_ID, TA_OPERATIONS.REMOVE)
    audience.update('/path/to/file', TA_LIST_TYPES.PHONE_NUMBER, TA_OPERATIONS.ADD)

    # delete the tailored audience
    audience.delete()

    # add users to the account's global opt-out list
    TailoredAudience.opt_out(account, '/path/to/file', TA_OPERATIONS.HANDLE)

def extractEmailsFromLeads(leadsList):
# Convert leadsList (python 'OrderedDict' datatype) to emailsList (python 'list' datatype)
    emailsList =[]
    #emailsList = leadsList['records'][i]['Email']
    for lead in leadsList['records']:
        emailsList.append(lead['Email'])
    return emailsList

def getLeadsListFromSalesforce(sfCred):
    salesforce_instance_url = sfCred['instance_url']
    salesforce_access_token = sfCred['access_token']
    salesforce_refresh_token = sfCred['refresh_token']

    # Login to SF
    sf = Salesforce(instance_url=salesforce_instance_url, session_id=salesforce_access_token)

    #import pytz
    #import datetime
    #end = datetime.datetime.now(pytz.UTC) # we need to use UTC as salesforce API requires this
    #sf.Contact.updated(end - datetime.timedelta(days=10), end)

    # Get leads list
    leadsList = getLeadsList(sf, sfCred)
    return leadsList

def getLeadsList(sf, sfCred):

    try:
        response = sf.query_all("SELECT Email FROM Lead WHERE Email <> ''")
    except Exception, e:
        if e.status == 401:
            SALESFORCE_REFRESH_URL = "https://login.salesforce.com/services/oauth2/token"
            SALESFORCE_CONSUMER_KEY = sfCred['consumer_key']   #"3MVG98_Psg5cppyYH7Cios03svOf9hpZtPg.n0yTXRIKlnjy43.MNRgdLDbmBc3T5wK2IoYOaPLNlqBzNouzE"
            SALESFORCE_CONSUMER_SECRET = sfCred['consumer_secret']   #"2132402812325087889"
            salesforce_refresh_token = sfCred['refresh_token']

            # HTTP request
            url = SALESFORCE_REFRESH_URL
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + sfCred['access_token'],
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
            db.pushSalseforceCredentials(sfCred)

            # try with new token
            sf = Salesforce(instance_url=sfCred['instance_url'], session_id=sfCred['access_token'])
            response = sf.query_all("SELECT Email FROM Lead WHERE Email <> ''")
    return response

def pushAdwordsCredentialsIfChanged(adwordsCred, new_adwords_access_token, new_adwords_refresh_token):
    flag = False
    if new_adwords_access_token != adwordsCred['access_token']:
        flag = True
        adwordsCred['access_token'] = new_adwords_access_token

    if new_adwords_refresh_token != adwordsCred['refresh_token']:
        flag = True
        adwordsCred['refresh_token'] = new_adwords_refresh_token

    if flag:
        db.pushAdwordsCredentials(adwordsCred)

def emailMsg(msg):
    import smtplib

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("3targeting@gmail.com", "ShedShvil11")

    server.sendmail("3targeting@gmail.com", "info@3targeting.com", msg)
    server.quit()
    return

def report2logfile(logfileName, msg):
    try:
        file = open(logfileName,'a')   # Append to logfile
        file.write(msg)
        file.close()
    except:
        print("Something went wrong at report2logfile: {}, {}").format(logfileName, msg)

def timestampGenerator():
    import time
    import datetime
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
    return timestamp



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
accountId = 3
#get instance_url & Access_token from Parse.com
# session_id='' == Access Token
"""
___________________ MySQL database ___________________
"""
# Register to db
db = mySQL.Database()

"""
______________________ Salesforce ______________________
"""

# Get SF credentials
sfCred = db.getSalesforceCredentials(accountId)
leadsList = getLeadsListFromSalesforce(sfCred)


"""
______________________ Report ______________________
"""
# report to logfile
timestamp = timestampGenerator()
msg = "Section: Salesforce   Action: Pulled X leads    Time:{}\n".format(timestamp)
report2logfile(LOG_FILE_NAME,msg)

# report by email
msg = "3Targeting just fetched leads list from another happy costumer"
#emailMsg(msg)


"""
_________________ Prepare Emails List _________________
lowercase & hash
"""

emailsList = extractEmailsFromLeads(leadsList)

# Normalize & Hash emails
hashedEmails = adWordsEmails.HashEmails(emailsList)

"""
_________________ AdWords _________________
"""

# get adWords credentials
adwordsCred = db.getAdwordsCredentials(accountId)
pushEmails2AdWords(hashedEmails, adwordsCred, db)


"""
_________________ Facebook _________________
"""
# get fb credentials
fbCred = db.getFacebookCredentials(accountId)
pushEmails2Facebook(hashedEmails,fbCred)


"""
#_________________ Twitter _________________
"""
twCred = db.getTwitterCredentials(accountId)
pushEmails2Twitter(hashedEmails,twCred)