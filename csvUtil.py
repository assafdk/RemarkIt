__author__ = 'assafdekel'

import csv, json
import time
import os

def makeDirIfNotExist(filename):
    dirName = os.path.dirname(filename)
    if not os.path.exists(dirName):
        os.makedirs(dirName)

def addRowToCSV(row, csvFileName):
    file = open(csvFileName, "a")
    csv_file = csv.writer(file)
    csv_file.writerow(row)
    file.close()
    return;

#accountName = "MazdaSalesPerson"
#exampleHeadersRow = ["header1", "header2", "header3", "header4", "header5", "header6", "header7"]
#exampleData = """[{"requestId": "334f#150ee2f0921", "success": true, "result": [{"annualRevenue": 10000.0, "leadScore": null, "numberOfEmployees": 2000, "industry": null, "priority": null, "firstName": "Mike", "id": 2, "personType": "contact"}, {"annualRevenue": null, "leadScore": null, "numberOfEmployees": null, "industry": null, "priority": null, "firstName": "yanir", "id": 7, "personType": "contact"}, {"annualRevenue": null, "leadScore": null, "numberOfEmployees": null, "industry": "Marketing", "priority": null, "firstName": "Grant", "id": 8, "personType": "contact"}]}]"""
#jsonData = json.loads(exampleData)

def makeHeadersList(headersRow):
    headersList = []
    indx = 0
    while indx != -1 :
        indx = headersRow.find(',')
        if indx == -1 :
            headersList.append(headersRow[:])
            break
        headersList.append(headersRow[:indx])
        headersRow = headersRow[indx+1:]
    return headersList

def json2csv(accountName ,dataDict, headersRow):
    print "json2csv"

    #dataDict = jsonData[0]
    isSuccess = dataDict['success']
    if not isSuccess:
        print "Bad http response from data source"
        exit(1)
    print "success"
    nowTime = time.strftime("%d-%b-%Y_%H.%M.%S", time.gmtime())
    dirName = time.strftime("%Y-%b-%d", time.gmtime())
    csvFileName = "%s/%s_%s.csv" % (dirName, accountName, nowTime)
    makeDirIfNotExist(csvFileName)
    headersRowList = makeHeadersList(headersRow)
    addRowToCSV(headersRowList, csvFileName)
    leadsList = dataDict["result"]
    for lead in leadsList:
        CsvRow = []
        for key, value in lead.items():
            CsvRow.append(value)
        addRowToCSV(CsvRow, csvFileName)
    return;
