__author__ = 'assafdekel'

from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.objects import AdUser

#Initialize a new Session and instanciate an Api object

my_app_id = '540991286064496'
my_app_secret = '5b4d044338217ad32a29852f194b09ad'
my_access_token = 'CAAHsB1lutXABAJ3THNIuYMpZCvDg5QOJp8PKRY8rzJqw45kIZBvVN8H30oMdvkYYHfH1z6uzCWaZC0HZCW7B10NcQMvyhkqzOq8e4Im2p342svV5PigbFkZCfjcpe7pW6FXjptLHCL0lZC4gSpGaIu0ZCv9H5S4MlnvkbsFQrTK0ZB83PtQDedZBYBrsXcPTPDDoiHGPY6J3qXQDOeu9pDuvL' # User access token
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

me = AdUser(fbid='me')
my_account = me.get_ad_accounts()[0]

print my_account


import requests
url = "https://graph.facebook.com/v2.5/act_{AD_ACCOUNT_ID}/customaudiences?access_token={ACCESS_TOKEN}".format(AD_ACCOUNT_ID = my_account['account_id'], ACCESS_TOKEN = my_access_token)
r = requests.get(url)
r.json()

print r

# # Create new audience
# URL = 'https://graph.facebook.com/v2.5/act_{AD_ACCOUNT_ID}/customaudiences'.format(AD_ACCOUNT_ID = my_account['account_id'])
# payload = {
#     'name' : 'test audience',
#     'subtype' : 'CUSTOM',
#     'description' : 'People who bought from my website',
#     'access_token' : my_access_token
# }
#
# session = requests.session()
# r = requests.post(URL, data=payload)


url = "https://graph.facebook.com/v2.5/act_{AD_ACCOUNT_ID}/customaudiences?access_token={ACCESS_TOKEN}".format(AD_ACCOUNT_ID = my_account['account_id'], ACCESS_TOKEN = my_access_token)
r = requests.get(url)
r.json()

print r

hash("sha256")