# connect to Parse.com
import urllib2, json
import csvUtil, mktoAPI, ParseAPI, GA_API
from parse_rest.connection import register
from parse_rest.datatypes import Object

# create Parse objects
class Task(Object):
    pass
class Job(Object):
    pass

# declare keys
APPLICATION_ID = "tZY8fKO4L7NkGEjviOW3O5PD5U9RNQEryLTJmQzi"
REST_API_KEY = "geuG8maGsRkbKskPulvxdCdaXGfnVz0uEZQLv1ZD"
MASTER_KEY = "62VZXS5bPyTh6Ny2QQEsYzziG1eKHdbWIYNutjzF"

def getLeedsJSON(job, munchkinID, accessToken):
	mktoQueryFields = ParseAPI.getMktoQueryFields(job)
	mktoResponseJson = mktoAPI.queryMkto(munchkinID, accessToken, mktoQueryFields)
	return mktoResponseJson


# Register to Parse.com DB
register(APPLICATION_ID, REST_API_KEY)

# Get all today's jobs
jobs = ParseAPI.getJobs()
# vars for loop
mktoCredentials = mktoAPI.MktoCredentials()
prevAccountId = None
for job in jobs:
	if ((prevAccountId == None) or (prevAccountId.objectId != job.account_id.objectId)):
		# Need new token
		mktoCredentials = ParseAPI.getMktoCredentials(job.account_id)
		mktoAccessToken = mktoAPI.getToken(mktoCredentials.munchkin, mktoCredentials.clientId, mktoCredentials.clientSecret)
	prevAccountId = job.account_id
	leedsJSON = getLeedsJSON(job, mktoCredentials.munchkin, mktoAccessToken)

	accountName = ParseAPI.getAccountName(job);
	headersRow = ParseAPI.getTargetHeaders(job);
	cvsFile = csvUtil.json2csv(accountName ,leedsJSON, headersRow)
	#GA_API.sendCsv2Target(cvsFile)


"""
mktoResponseJson = None
mktoQuery = None
for job in jobs:
	# first try to continue querying mkto. If can't -> get new token + queryURL
	try:
		queryParams == ParseAPI.getQueryParameters()
		mktoQueryURL = mktoAPI.getMktoQueryURL(queryParams)
		mktoResponse = urllib2.urlopen(mktoQuery)
		mktoResponseJson = json.load(mktoResponse)
	except:
		# bad mktoQuery URL -> generate new one
		munchkinID = "777-JUM-540" #account Id
		customServiceClientId = "7cd8197b-0e87-4b0f-a7ff-4354100fb2b2"
		customServiceClientSecret = "YfdzX9c5pEoYypF29oduFt9Ycp6KDdkz"
		#4. User - api-marketortp@marketortp.com

		accessToken = mktoAPI.getToken(munchkinID, customServiceClientId, customServiceClientSecret)
		mktoResponseJson = mktoAPI.queryMkto(munchkinID, accessToken)


	isValid = mktoAPI.isValid(mktoResponseJson)




	if mktoAPI.isValidResponse(mktoResponseJson):






	print mktoResponse
	print ""
	jsonData = json.load(mktoResponse)
	print jsonData
	print ""
	accountName = "MazdaSalesPerson"
	exampleHeadersRow = ["header1", "header2", "header3", "header4", "header5", "header6", "header7"]
	csvFile = csvUtil.json2csv(accountName ,jsonData, exampleHeadersRow)



parseAPI.getCredentials()












# 2. read all tasks from Pasre.com DB
all_tasks = Task.Query.all()

# for every task
for task in all_tasks:
# 3. query mkto
	mktoResponse = urllib2.urlopen(task.mktoQuery)
	print mktoResponse
	print ""
	jsonData = json.load(mktoResponse)
	print jsonData
	print ""
	accountName = "MazdaSalesPerson"
	exampleHeadersRow = ["header1", "header2", "header3", "header4", "header5", "header6", "header7"]
	csvFile = csvUtil.json2csv(accountName ,jsonData, exampleHeadersRow)
	#gglResponse = urllib2.urlopen(task.gglQuery)


#https://777-JUM-540.mktorest.com/rest/v1/leads.json?access_token=c1572008-f002-4f45-bc8a-7daefa512fd8:sj&filterType=id&filterValues=1,2,3,4,5,6,7,8,9,10,11,12,13&fields=leadScore,priority,firstName,personType,annualRevenue,numberOfEmployees,industry&batchSize=100&_method=GET




"""

"""
1. connect to Parse.com
2. read all tasks
3. for every task
	3.1. query mkto
	3.2. get JSON response
	3.3. parse from JSON to CSV
	3.4. send to ggl
"""
