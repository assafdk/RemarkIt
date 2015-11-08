from parse_rest.connection import register

APPLICATION_ID = "tZY8fKO4L7NkGEjviOW3O5PD5U9RNQEryLTJmQzi"
REST_API_KEY = "geuG8maGsRkbKskPulvxdCdaXGfnVz0uEZQLv1ZD"
MASTER_KEY = "62VZXS5bPyTh6Ny2QQEsYzziG1eKHdbWIYNutjzF"

register(APPLICATION_ID, REST_API_KEY)

# create objects
from parse_rest.datatypes import Object
class Task(Object):
    pass

# single object query
task = Task.Query.get(objectId="Bjx2ISq53B")

print task.createdAt
print task.objectId
print task.gglQuery


# query all
all_tasks = Task.Query.all()

print all_tasks

for task in all_tasks:
	print task.mktoQuery


import csv

changes = [    
    ['1 dozen','12'],                                                            
    ['1 banana','13'],                                                           
    ['1 dollar','elephant','heffalump'],                                         
    ]                                                                            

with open('test.csv', 'ab') as f:                                    
    writer = csv.writer(f)                                                       
    writer.writerows(changes)



# {}{}{} Strategy {}{}{}
all_tasks = getAllTasks()
for task in all_tasks:
	costumerObjects = run_mktoQuery(task)
	costumerCSV = createCSV(costumerObjects)
	run_gglQuery(task.gglQuery, costumerCSV)


def getAllTasks():
	all_tasks = Task.Query.all()
	return all_tasks;