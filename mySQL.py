__author__ = 'assafdekel'
import json
import mysql.connector

class Database:

    cnx = mysql.connector

    def __init__(self):
        self.cnx = mysql.connector.connect(user='locatit6_3yc', password='ShedShvil11',
                                           host='50.87.248.155',
                                           database='locatit6_3targeting')
    def __del__(self):
        self.cnx.close()

    def closeConnection(self):
        self.cnx.close()

    def getSalesforceCredentials(self, accountId):
        cursor = self.cnx.cursor()
        query = ("SELECT id, account_name, sfdc_access_token, sfdc_refresh_token, sfdc_consumer_key, sfdc_instance_url FROM accounts WHERE id = {}").format(accountId)
        cursor.execute(query)
        result = cursor.fetchall()
        colNames = cursor.column_names

        for row in result:
            sfCred = {} # credentials dictionary
            sfCred['id'] = row[0]
            sfCred['account_name'] = row[1]
            sfCred['sfdc_access_token'] = row[2]
            sfCred['sfdc_refresh_token'] = row[3]
            sfCred['sfdc_consumer_key'] = row[4]
            sfCred['sfdc_instance_url'] = row[5]

        # for account in cursor:
        #     sf_access_token = account.sfdc_access_token
        #     sf_refresh_token = sfdc_refresh_token
        #     sf_id = sfdc_id
        #     sf_instance_url = sfdc_instance_url


        cursor.close()
        return sfCred


    def getAdwordsCredentials(self, accountId):
        cursor = self.cnx.cursor()
        query = ("SELECT id, account_name, adwords_access_token, adwords_refresh_token FROM accounts WHERE id = {}").format(accountId)
        cursor.execute(query)
        result = cursor.fetchall()
        colNames = cursor.column_names

        for row in result:
            adwordsCred = {} # credentials dictionary
            adwordsCred['id'] = row[0]
            adwordsCred['account_name'] = row[1]
            adwordsCred['adwords_access_token'] = row[2]
            adwordsCred['adwords_refresh_token'] = row[3]

        cursor.close()
        return adwordsCred

    def getFacebookCredentials(self, accountId):
        cursor = self.cnx.cursor()
        query = ("SELECT id, account_name, fb_user_id, fb_account_id, fb_user_token, fb_expiresIn, fb_spent FROM accounts WHERE id = {}").format(accountId)
        cursor.execute(query)
        result = cursor.fetchall()
        colNames = cursor.column_names

        for row in result:
            fbCred = {} # credentials dictionary
            fbCred['id'] = row[0]
            fbCred['account_name'] = row[1]
            fbCred['fb_user_id'] = row[2]
            fbCred['fb_account_id'] = row[3]
            fbCred['fb_user_token'] = row[4]
            fbCred['fb_expiresIn'] = row[5]
            fbCred['fb_spent'] = row[6]

        cursor.close()
        return fbCred

    def query(self, queryStr):
        cursor = self.cnx.cursor()
        cursor.execute(queryStr)

        cursor.close()
        self.cnx.close()



# --- DEBUG ---
#a = Database()
#print a

#
# V def getAdwordsCredentials(accountId):
#     userCredentials = accounts.Query.get(objectId=accountId)
#     return userCredentials.adwords
#
# V def getFacebookCredentials(accountId):
#     userCredentials = accounts.Query.get(objectId=accountId)
#     return userCredentials.facebook
#
#
#
#     def pushAdwordsCredentials(accountId, gglAccessToken, gglRefreshToken):
# 	adwordsCredentials = {'active':True, 'access_token':gglAccessToken, 'refresh_token':gglRefreshToken}
# 	# encode as a JSON-like string
# 	adwordsCredentials = json.loads(json.dumps(adwordsCredentials))
# 	adwordAccount  = accounts(objectId=accountId,adwords=adwordsCredentials)
# 	adwordAccount.save()
#
# def pushSalesforceCredentials(accountId, jsonCredentials):
# 	salesforceAccount  = accounts(objectId=accountId,salesforce=jsonCredentials)
# 	salesforceAccount.save()
#
# # def getCredentials(service, accountId):
# #     serviceClass = Object.factory(service)
# #     userCredentials = accounts.Query.get(objectId=accountId)
# #     retval = userCredentials[service]
#
#
#
# # def getJobs():
# #     local_jobs = jobs.Query.all()
# #     return local_jobs;
# #
# # def getAccountName(job):
# #     accountId = job.account_id.objectId
# #     accountName = accounts.Query.get(objectId=accountId)
# #     return accountName.name
# #
# # def getTargetHeaders(job):
# #     targetId = job.target_query_id.objectId
# #     queryRow = queries.Query.get(objectId=targetId)
# #     return queryRow.query_sql
# #
# # def getMktoQueryFields(job):
# #     datasourceQueryId = job.datasource_query_id.objectId
# #     queryobject = queries.Query.get(objectId=datasourceQueryId)
# #     queryFields = queryobject.query_sql
# #     return queryFields;
# #
# # def getMktoCredentials(accountId):
# #     # var
# #     mktoCredentials = mktoAPI.MktoCredentials()
# #
# #     local_credentials = credentials.Query.get(account_id=accountId)
# #     mktoCredentials.munchkin = local_credentials.marketo_munchkin
# #     mktoCredentials.clientId = local_credentials.marketo_clientid
# #     mktoCredentials.clientSecret = local_credentials.marketo_client_secret
# #     return mktoCredentials;
# #
# # """
# # 1. get Jobs
# # 2. from job -> datasource_query_id
# # 3. from Qeuries table -> query(objectId = datasource_query_id)
# # 4. from query -> query_sql (this is the filter)
# #
# # if queryURL is no longer valid
# # Tokens:
# # 1. my_account_id = job.account_id
# # 2. my_credentials = Credentials.get(my_account_id)
# # 3. my_credentials.marketo_clientid
# #
# # """