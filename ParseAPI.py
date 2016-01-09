__author__ = 'assafdekel'
from parse_rest.connection import register
from parse_rest.datatypes import Object
import json
import mktoAPI

# # declare keys
# APPLICATION_ID = "tZY8fKO4L7NkGEjviOW3O5PD5U9RNQEryLTJmQzi"
# REST_API_KEY = "geuG8maGsRkbKskPulvxdCdaXGfnVz0uEZQLv1ZD"
# MASTER_KEY = "62VZXS5bPyTh6Ny2QQEsYzziG1eKHdbWIYNutjzF"

# declare keys
APPLICATION_ID = "zEw8OuVGoLit8vfLuofQZuKAJa6TIWTgKmInIt1F"
REST_API_KEY = "VZWgc30TFeResXW0oOHW21haVMSkiZXugm2hO72L"
#MASTER_KEY = "PeCO4elOGe1Inreo6g9WZkmdRxCon8EkDLbxDkIv"

class test_credentials(Object):
    pass

class accounts(Object):
    pass

class jobs(Object):
    pass
class queries(Object):
    pass
class credentials(Object):
    pass


def register2remoteDB():
    # 1. register to Parse.com DB
    register(APPLICATION_ID, REST_API_KEY)

def pushAdwordsCredentials(accountId, gglAccessToken, gglRefreshToken):
	adwordsCredentials = {'active':True, 'access_token':gglAccessToken, 'refresh_token':gglRefreshToken}
	# encode as a JSON-like string
	adwordsCredentials = json.loads(json.dumps(adwordsCredentials))
	adwordAccount  = accounts(objectId=accountId,adwords=adwordsCredentials)
	adwordAccount.save()

def pushSalesforceCredentials(accountId, jsonCredentials):
	salesforceAccount  = accounts(objectId=accountId,salesforce=jsonCredentials)
	salesforceAccount.save()

# def getCredentials(service, accountId):
#     serviceClass = Object.factory(service)
#     userCredentials = accounts.Query.get(objectId=accountId)
#     retval = userCredentials[service]

def getSalesforceCredentials(accountId):
    userCredentials = accounts.Query.get(objectId=accountId)
    return userCredentials.salesforce


# def getJobs():
#     local_jobs = jobs.Query.all()
#     return local_jobs;
#
# def getAccountName(job):
#     accountId = job.account_id.objectId
#     accountName = accounts.Query.get(objectId=accountId)
#     return accountName.name
#
# def getTargetHeaders(job):
#     targetId = job.target_query_id.objectId
#     queryRow = queries.Query.get(objectId=targetId)
#     return queryRow.query_sql
#
# def getMktoQueryFields(job):
#     datasourceQueryId = job.datasource_query_id.objectId
#     queryobject = queries.Query.get(objectId=datasourceQueryId)
#     queryFields = queryobject.query_sql
#     return queryFields;
#
# def getMktoCredentials(accountId):
#     # var
#     mktoCredentials = mktoAPI.MktoCredentials()
#
#     local_credentials = credentials.Query.get(account_id=accountId)
#     mktoCredentials.munchkin = local_credentials.marketo_munchkin
#     mktoCredentials.clientId = local_credentials.marketo_clientid
#     mktoCredentials.clientSecret = local_credentials.marketo_client_secret
#     return mktoCredentials;
#
# """
# 1. get Jobs
# 2. from job -> datasource_query_id
# 3. from Qeuries table -> query(objectId = datasource_query_id)
# 4. from query -> query_sql (this is the filter)
#
# if queryURL is no longer valid
# Tokens:
# 1. my_account_id = job.account_id
# 2. my_credentials = Credentials.get(my_account_id)
# 3. my_credentials.marketo_clientid
#
# """