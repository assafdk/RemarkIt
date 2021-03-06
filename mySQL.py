__author__ = 'assafdekel'
import MySQLdb

class Database:

    db = MySQLdb.Connection

    def __init__(self):
        # BlueHost
        # self.db = MySQLdb.connect(host='50.87.248.155',
        #                            user='locatit6_3yc',
        #                            passwd='ShedShvil11',
        #                            db='locatit6_3targeting')

        # AWS RDS
        self.db = MySQLdb.connect(host='ncal-mysql-instance1.caabsuivlzcf.us-west-1.rds.amazonaws.com',
                                   user='aws3targeting',
                                   passwd='ShedShvil11',
                                   db='mysql3targeting')

    # def __del__(self):
    #     self.db.close()
    #
    # def closeConnection(self):
    #     self.db.close()

    def getJobsList(self):
        cursor = self.db.cursor()
        query = ("SELECT id, account_id, job_name, job_description, audience, cycle, last_run, in_sf, out_fb, out_twitter, out_aw, out_ga, time_created, time_updated, created_by FROM jobs")
        cursor.execute(query)
        jobsList = cursor.fetchall()
        cursor.close()
        return jobsList


    def parseJob(self, row):
        job = {} # job dictionary
        job['id'] = row[0]
        job['account_id'] = row[1]
        job['job_name'] = row[2]
        job['job_description'] = row[3]
        job['audience'] = row[4]
        job['cycle'] = row[5]
        job['last_run'] = row[6]
        job['in_sf'] = row[7]
        job['out_fb'] = row[8]
        job['out_twitter'] = row[9]
        job['out_aw'] = row[10]
        job['out_ga'] = row[11]
        job['time_created'] = row[12]
        job['time_updated'] = row[13]
        job['created_by'] = row[14]
        return job

    def getAudience(self, job):
        cursor = self.db.cursor()
        query = ("SELECT id, account_id, audience_name, audience_description, audience_type, last_run, sql_select, sql_where, aw_user_list_id, fb_user_list_id, tw_user_list_id, ga_user_list_id, time_created, time_updated, created_by FROM audiences WHERE id = {}").format(job['audience'])
        cursor.execute(query)
        result = cursor.fetchall()

        row = result[0]
        audience = {} # job dictionary
        audience['id'] = row[0]
        audience['account_id'] = row[1]
        audience['audience_name'] = row[2]
        audience['audience_description'] = row[3]
        audience['audience_type'] = row[4]
        audience['last_run'] = row[5]
        audience['sql_fields'] = row[6]
        audience['sql_filter_phrase'] = row[7]
        audience['sql_query'] = ("SELECT " + row[6] + " from Lead WHERE " + row[7] )
        audience['aw_user_list_id'] = row[8]
        audience['fb_user_list_id'] = row[9]
        audience['tw_user_list_id'] = row[10]
        audience['ga_user_list_id'] = row[11]
        audience['time_created'] = row[12]
        audience['time_updated'] = row[13]
        audience['created_by'] = row[14]

        cursor.close()
        return audience

    def getSalesforceCredentials(self, accountId):
        cursor = self.db.cursor()
        query = ("SELECT consumer_key, consumer_secret, access_token, instance_url, refresh_token, sf_id, issued_at, scope, signature, token_type, enabled FROM sf_credentials WHERE account_id = {}").format(accountId)
        cursor.execute(query)
        result = cursor.fetchall()

        for row in result:
            sfCred = {} # credentials dictionary
            sfCred['accountId'] = accountId
            sfCred['consumer_key'] = row[0]
            sfCred['consumer_secret'] = row[1]
            sfCred['access_token'] = row[2]
            sfCred['instance_url'] = row[3]
            sfCred['refresh_token'] = row[4]
            sfCred['sf_id'] = row[5]
            sfCred['issued_at'] = row[6]
            sfCred['scope'] = row[7]
            sfCred['signature'] = row[8]
            sfCred['token_type'] = row[9]
            sfCred['enabled'] = row[10]

        # for account in cursor:
        #     sf_access_token = account.sfdc_access_token
        #     sf_refresh_token = sfdc_refresh_token
        #     sf_id = sfdc_id
        #     sf_instance_url = sfdc_instance_url


        cursor.close()
        return sfCred

    def getAdwordsCredentials(self, accountId):
        cursor = self.db.cursor()
        query = ("SELECT enabled, access_token, refresh_token, user_list_id FROM adwords_credentials WHERE account_id = {}").format(accountId)
        cursor.execute(query)
        result = cursor.fetchall()

        for row in result:
            adwordsCred = {} # credentials dictionary
            adwordsCred['accountId'] = accountId
            adwordsCred['enabled'] = row[0]
            adwordsCred['access_token'] = row[1]
            adwordsCred['refresh_token'] = row[2]
            adwordsCred['user_list_id'] = row[3]

        cursor.close()
        return adwordsCred

    def getFacebookCredentials(self, accountId):
        cursor = self.db.cursor()
        query = ("SELECT enabled, fb_user_id, fb_account_id, user_token, expiresIn, spent FROM fb_credentials WHERE account_id = {}").format(accountId)
        cursor.execute(query)
        result = cursor.fetchall()

        for row in result:
            fbCred = {} # credentials dictionary
            fbCred['accountId'] = accountId
            fbCred['enabled'] = row[0]
            fbCred['fb_user_id'] = row[1]
            fbCred['fb_account_id'] = row[2]
            fbCred['user_token'] = row[3]
            fbCred['expiresIn'] = row[4]
            fbCred['spent'] = row[5]

        cursor.close()
        return fbCred

    def pushSalseforceCredentials(self, sfCred):
        cursor = self.db.cursor()
        query = ("UPDATE sf_credentials SET access_token = '" + sfCred['access_token']
                 + "', refresh_token = '" + sfCred['refresh_token']
                 + "', instance_url = '" + sfCred['instance_url']
                 + "', sf_id = '" + sfCred['sf_id']
                 + "', issued_at = '" + sfCred['issued_at']
                 + "', scope = '" + sfCred['scope']
                 + "', signature = '" + sfCred['signature']
                 + "', token_type = '" + sfCred['token_type']
                 + "' WHERE account_id = {}").format(sfCred['accountId'])
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        return

    def pushFacebookCredentials(self, fbCred):
        cursor = self.db.cursor()
        query = ("UPDATE fb_credentials SET user_token = '" + fbCred['user_token']
                 + "', expiresIn = '" + fbCred['expiresIn']
                 + "', spent = '" + fbCred['spent']
                 + "' WHERE account_id = {}").format(fbCred['accountId'])

        cursor.execute(query)
        self.db.commit()
        cursor.close()
        return

    def pushAdwordsCredentials(self, awCred):
        cursor = self.db.cursor()
        # query = "UPDATE adwords_credentials SET access_token = '" + awCred['access_token'] \
        #         + "', refresh_token = '" + awCred['refresh_token'] \
        #         + "', user_list_id = {}'" \
        #         + "' WHERE account_id = {}".format(awCred['user_list_id'], awCred['accountId'])
        query = "UPDATE adwords_credentials SET access_token = '" + awCred['access_token'] \
                + "', refresh_token = '" + awCred['refresh_token'] \
                + "', user_list_id = {} WHERE account_id = {}".format(awCred['user_list_id'], awCred['accountId'])
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        return

    # def pushTwitterCredentials(self, accountId, twitterCred):
    #     cursor = self.db.cursor()
    #     query = ("UPDATE accounts SET fb_user_id=twitterCred['fb_user_id'], fb_account_id=twitterCred['fb_account_id'], fb_user_token=twitterCred['fb_user_token'], fb_expiresIn=twitterCred['fb_expiresIn'], fb_spent=twitterCred['fb_spent'] WHERE id = {}").format(accountId)
    #     cursor.execute(query)
    #     cursor.close()
    #     return


# # debug
# a = Database()
# accountId = 1
#
# sfCred = {}
# sfCred['accountId'] = '1'
# sfCred['access_token'] = '1'
# sfCred['refresh_token'] = '1'
# sfCred['instance_url'] = '1'
# sfCred['sf_id'] = '1'
# sfCred['issued_at'] = '1'
# sfCred['scope'] = '1'
# sfCred['signature'] = '1'
# sfCred['token_type'] = '1'
#
# fbCred = {}
# fbCred['accountId'] = '1'
# fbCred['user_token'] = '1'
# fbCred['expiresIn'] = '1'
# fbCred['spent'] = '1'
#
# awCred = {}
# awCred['accountId'] = '1'
# awCred['access_token'] = '1'
# awCred['refresh_token'] = '1'
#
# print a
#
