__author__ = 'Assaf Dekel'

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

sf = Salesforce(instance_url=salesforce_instance_url, session_id=salesforce_access_token)
response = sf.query_all("SELECT Id, Email FROM Lead WHERE LastName = 'Abbott'")

emailsList = []
#response['records'][i]['Email']
for lead in response['records']:
    emailsList.append(lead['Email'])





print emailsList
sfCred = parse.getSalesforceCredentials()


sfCred.instance_url
sfCred.access_token

#sf = Salesforce(instance_url=sfCred.instance_url, session_id=sfCred.access_token)
#sf = Salesforce(instance_url='https://na1.salesforce.com', session_id='')


#import pytz
#import datetime
#end = datetime.datetime.now(pytz.UTC) # we need to use UTC as salesforce API requires this
#sf.Contact.updated(end - datetime.timedelta(days=10), end)


#sf.query_all("SELECT Id, Email FROM Contact WHERE LastName = 'Jones'")