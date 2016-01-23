#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Initializes an AdWordsClient without using yaml-cached credentials.

While our LoadFromStorage method provides a useful shortcut to instantiate a
client if you regularly use just one set of credentials, production applications
may need to swap out users. This example shows you how to create an OAuth 2.0
client and an AdWordsClient without relying on a yaml file.
"""


from googleads import adwords
from googleads import oauth2

test_CLIENT_CUSTOMER_ID = '543-963-1369'
production_CLIENT_CUSTOMER_ID = '393-270-7738'

# OAuth 2.0 credential information. In a real application, you'd probably be
# pulling these values from a credential storage.
CLIENT_ID = '280160838890-kjhls6qlss26fj1f2kr7v61fh5esmmuk.apps.googleusercontent.com'
CLIENT_SECRET = 'ZQLzF8TadPS3Zpk52rACGsKG'
REFRESH_TOKEN = '1/-cU8qsogyXoHAHGQ4GnpGOUBvNR375Oz6dJY7xHSfAQ'

# AdWords API information.
DEVELOPER_TOKEN = 'YAVzDP8OR2vtzQ_Bp_ztFA'
USER_AGENT = '3Targeting'
CLIENT_CUSTOMER_ID = test_CLIENT_CUSTOMER_ID

def login(client_id, client_secret, refresh_token, developer_token, user_agent,
         client_customer_id):
  oauth2_client = oauth2.GoogleRefreshTokenClient(
      client_id, client_secret, refresh_token)

  adwords_client = adwords.AdWordsClient(
      developer_token, oauth2_client, user_agent, client_customer_id)

  customer = adwords_client.GetService('CustomerService').get()
  print 'You are logged in as customer: %s' % customer['customerId']

  new_access_token = adwords_client.oauth2_client.oauth2credentials.access_token
  new_refresh_token = adwords_client.oauth2_client.oauth2credentials.refresh_token
  return [adwords_client, new_access_token, new_refresh_token]

if __name__ == '__main__':
  login(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, DEVELOPER_TOKEN, USER_AGENT,
       CLIENT_CUSTOMER_ID)