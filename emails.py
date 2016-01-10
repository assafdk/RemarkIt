__author__ = 'Assaf Dekel'

import requests, json
import ParseAPI as parse
from simple_salesforce import Salesforce


"""
V 1.register to parse
  2.Get all active users from Parse
  for each user:
V 3.Get SF credentials
V 4.connect to SF
V 5.get leads list
V 6.convert to emailsList
 7.convert to google AdWords format
 8.send to google AdWords
"""
user_account = "IXcARxYdJF"

#get instance_url & Access_token from Parse.com
# session_id='' == Access Token

parse.register2remoteDB()
sfCred = parse.getSalesforceCredentials(user_account)
salesforce_instance_url = sfCred['instance_url']
salesforce_access_token = sfCred['access_token']
salesforce_refresh_token = sfCred['refresh_token']

sf = Salesforce(instance_url=salesforce_instance_url, session_id=salesforce_access_token)

#import pytz
#import datetime
#end = datetime.datetime.now(pytz.UTC) # we need to use UTC as salesforce API requires this
#sf.Contact.updated(end - datetime.timedelta(days=10), end)

try:
    response = sf.query_all("SELECT Id, Email FROM Lead WHERE LastName = 'Abbott'")
except Exception, e:
    if e.status == 401:
        SALESFORCE_REFRESH_URL = "https://login.salesforce.com/services/oauth2/token"
        SALESFORCE_CONSUMER_KEY = "3MVG98_Psg5cppyYH7Cios03svOf9hpZtPg.n0yTXRIKlnjy43.MNRgdLDbmBc3T5wK2IoYOaPLNlqBzNouzE"
        SALESFORCE_CONSUMER_SECRET = "2132402812325087889"
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
        response = sf.query_all("SELECT Id, Email FROM Lead WHERE LastName = 'Abbott'")


emailsList = []
#response['records'][i]['Email']
for lead in response['records']:
    emailsList.append(lead['Email'])


"""
From her: Google AdWords -> make emails list and upload
"""
