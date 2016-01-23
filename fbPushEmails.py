__author__ = 'assafdekel'

from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.objects import AdUser

#Initialize a new Session and instanciate an Api object

my_app_id = '540991286064496'
my_app_secret = '5b4d044338217ad32a29852f194b09ad'
my_access_token = 'CAAHsB1lutXABALDJ3TahbUe1A8lEJpHkQhSQe4yXdC0xg6l0zNCnsAAQeVD4QGl84G0UP279ZCLRZByXmHIdGFQE4MohJPcBZAV1Wdjk6BdZCJZB5yBlmaBx3AZAF3QmFoxNZBoBVTemNrrI2Owd31S09cb4qOKZAqwZAoXo38ZBXmqOrE8i20NgmZB4znXBA3uSN4rkpaFWOhOYY7j4EcOUu2D' # User access token
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

me = AdUser(fbid='me')
my_account = me.get_ad_accounts()[0]

print my_account