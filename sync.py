from parse_rest.connection import register

APPLICATION_ID = "tZY8fKO4L7NkGEjviOW3O5PD5U9RNQEryLTJmQzi"
REST_API_KEY = "geuG8maGsRkbKskPulvxdCdaXGfnVz0uEZQLv1ZD"
MASTER_KEY = "62VZXS5bPyTh6Ny2QQEsYzziG1eKHdbWIYNutjzF"

register(APPLICATION_ID, REST_API_KEY)

# create Parse objects
from parse_rest.datatypes import Object
class Task(Object):
    pass

# create http request tool
import urllib2
response = urllib2.urlopen('http://python.org/')
html = response.read()




def run_mktoQuery(task):
    response = '{"requestId": "6ad8#150eb10470e",\
            "result": [\
                {\
                    "id": 2,\
                    "leadScore": 20,\
                    "annualRevenue": 10000,\
                    "priority": none,\
                    "numberOfEmployees": 2000,\
                    "industry": "Education",\
                    "personType": "contact",\
                    "firstName": "Mike"\
                },\
                {\
                    "id": 7,\
                    "leadScore": null,\
                    "annualRevenue": 1000000,\
                    "priority": null,\
                    "numberOfEmployees": null,\
                    "industry": null,\
                    "personType": "contact",\
                    "firstName": "yanir"\
                },\
                {\
                    "id": 8,\
                    "leadScore": null,\
                    "annualRevenue": null,\
                    "priority": high,\
                    "numberOfEmployees": 1000,\
                    "industry": "Marketing",\
                    "personType": "contact",\
                    "firstName": "Grant"\
                }\
            ],\
            "success": true\
        }'
    return response
    








# single object query
task = Task.Query.get(objectId="Bjx2ISq53B")

print task.createdAt
print task.objectId
print task.gglQuery


res = run_mktoQuery(task)
print "response is ..."
print res

# query all
all_tasks = Task.Query.all()

print all_tasks

for task in all_tasks:
	print task.mktoQuery





# {}{}{} Strategy {}{}{}
#all_tasks = getAllTasks()
#for task in all_tasks:
	#costumerObjects = run_mktoQuery(task)
	#costumerCSV = createCSV(costumerObjects)
	#run_gglQuery(task.gglQuery, costumerCSV)


def getAllTasks():
	all_tasks = Task.Query.all()
	return all_tasks;


"""
def createCSV(costumerObjects):
    import csv

    changes = [    
        ['1 dozen','12'],                                                            
        ['1 banana','13'],                                                           
        ['1 dollar','elephant','heffalump'],                                         
        ]                                                                            

    with open('test.csv', 'ab') as f:                                    
        writer = csv.writer(f)                                                       
        writer.writerows(changes)

        return "test.csv"
"""