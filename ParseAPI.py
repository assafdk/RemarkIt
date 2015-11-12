__author__ = 'assafdekel'
from parse_rest.connection import register
from parse_rest.datatypes import Object
import mktoAPI

# declare keys
APPLICATION_ID = "tZY8fKO4L7NkGEjviOW3O5PD5U9RNQEryLTJmQzi"
REST_API_KEY = "geuG8maGsRkbKskPulvxdCdaXGfnVz0uEZQLv1ZD"
MASTER_KEY = "62VZXS5bPyTh6Ny2QQEsYzziG1eKHdbWIYNutjzF"

class jobs(Object):
    pass
class queries(Object):
    pass
class credentials(Object):
    pass

def __init__(self):
    # 1. register to Parse.com DB
    register(APPLICATION_ID, REST_API_KEY)

def getJobs():
    local_jobs = jobs.Query.all()
    return local_jobs;

def getMktoQueryFields(job):
    datasourceQueryId = job.datasource_query_id.objectId
    queryobject = queries.Query.get(objectId=datasourceQueryId)
    queryFields = queryobject.query_sql
    return queryFields;

def getMktoCredentials(accountId):
    # var
    mktoCredentials = mktoAPI.MktoCredentials()

    local_credentials = credentials.Query.get(account_id=accountId)
    mktoCredentials.munchkin = local_credentials.marketo_munchkin
    mktoCredentials.clientId = local_credentials.marketo_clientid
    mktoCredentials.clientSecret = local_credentials.marketo_client_secret
    return mktoCredentials;

"""
1. get Jobs
2. from job -> datasource_query_id
3. from Qeuries table -> query(objectId = datasource_query_id)
4. from query -> query_sql (this is the filter)

if queryURL is no longer valid
Tokens:
1. my_account_id = job.account_id
2. my_credentials = Credentials.get(my_account_id)
3. my_credentials.marketo_clientid

"""