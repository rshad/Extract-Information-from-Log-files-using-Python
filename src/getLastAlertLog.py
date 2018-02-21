#!/usr/bin/python
#Execute command: $ python getLastAlertLog.py -i ../data/alerts.log -o ../output/lastAlert.txt -d 2018/01/14
import sys, getopt, os
import datetime
import time
from operator import itemgetter #sorted

def januar():
    return "1"
def february():
    return "2"
def march():
    return "3"
def april():
    return "4"
def may():
    return "5"
def june():
    return "6"
def july():
    return "7"
def august():
    return "8"
def september():
    return "9"
def octuber():
    return "10"
def december():
    return "11"
def november():
    return "12"

#convert month from name to number format
monthsTimstamp = {"Jan" : januar(),
    "Feb" : february(),
    "Mar" : march(),
    "Apr" : april(),
    "May" : may(),
    "Jun" : june(),
    "Jul" : july(),
    "Aug" : august(),
    "Sep" : september(),
    "Oct" : octuber(),
    "Nov" : november(),
    "Des" : december()
}

#get the alerts with the same year
def getSameYearList(lista,year):
    auxList = []
    for dic in lista:
        if dic["timestamp"]["year"] == year:
            auxList.append(dic.copy())
    return auxList

#then get the alerts with same month
def getSameMonthList(sameYearLista,month):
    auxList = []
    for dic in sameYearLista:
        if dic["timestamp"]["month"] == month:
            auxList.append(dic.copy())
    return auxList
#finally get the alerts with the same day
def getSameDayList(sameYearMonthLista,day):
    auxList = []
    for dic in sameYearMonthLista:
        if dic["timestamp"]["day"] == day:
            auxList.append(dic.copy())
    return auxList

#main function
def main(argv):
    #set input parameters
    inputfile = ''
    outputfile = ''
    date = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:d:", ["ifile=", "ofile=", "ntable="])
    except getopt.GetoptError:
        print 'getLastAlertLog.py -i <inputfile> -o <outputfile> -d <date>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile> -d <date>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d", "--ntable"):
            date = arg

    if(inputfile=="" or outputfile=="" or date==""):
        print("----->> Warning <<-----")
        print("'getLastAlertLog.py -i <inputfile> -o <outputfile> -d YYYY/MM/DD'")
    else:
        print("****Input parameters****")
        print "input= " + inputfile
        print "output= " + outputfile
        print "date= " + date
        print("------------------------")

        #read the input file
        lines = [line for line in open(inputfile)]

        alert = {}
        jsonLista = []
        for l in lines:
            #get the inode (the last feature)
            if any("inode" in s for s in l.split(" ")):
                lista = l.split(":")
                alert["inode"] = lista[1].strip('\n')
                jsonLista.append(alert.copy())
                alert = {}# its the last feature so we clean the dic
            #get timestamp
            elif any("->" in s for s in l.split(" ")) and not (any("Rule" in s for s in l.split(" "))):
                lista = l.split("->")
                yearTimestamp = lista[0].split(" ")[0]
                monthTimestamp = monthsTimstamp[lista[0].split(" ")[1]]
                dayTimestamp = lista[0].split(" ")[2]
                timeTimestamp = lista[0].split(" ")[3]
                timestamp = {}
                timestamp["year"] = int(yearTimestamp)
                timestamp["month"] = int(monthTimestamp)
                timestamp["day"] = int(dayTimestamp)
                timestamp["time"] = timeTimestamp
                #convert the time hour+minutes+seconds to seconds, this will be useful to get the last alert
                x = time.strptime(timeTimestamp, '%H:%M:%S')
                y = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
                alert["totalSeconds"] = int(y)
                alert["timestamp"] = timestamp
                timestamp = {}
            #get rule and level features
            elif (any("Rule" in s for s in l.split(" "))):
                rule = l.split(":")[1].split("(")[0]
                level = l.split(":")[1].split("level")[1].split(")")[0]
                alert["level"] = level
                alert["rule"] = rule
            #get the rest of features
            elif l != '\n' and not (any("added" in s for s in l.split(" "))):
                lista = l.split(":")
                if len(lista[0].split(" ")) >= 2:
                    alert[lista[0].split(" ")[1]] = lista[1].strip('\n')
                else:
                    alert[lista[0]] = lista[1].strip('\n')
        #date parameter
        yearParameter = int(date.split("/")[0])
        monthParameter = int(date.split("/")[1])
        dayParameter = int(date.split("/")[2])

        #get ther alerts which have timestamp equal to the date parameter
        sameYear = getSameYearList(jsonLista,yearParameter)
        sameYearMonth = getSameMonthList(sameYear,monthParameter)
        sameYearMonthDay = getSameDayList(sameYearMonth,dayParameter)

        #sort the results alerts depends the time in reverse orden
        sortedList = sorted(sameYearMonthDay, key=itemgetter('totalSeconds'),reverse=True)

        #get the last alert (the first one in the sorted list)
        lastAlert = sortedList[0]

        #write the result in the output file
        """
        lastAlertOutput = open(outputfile, 'w')
        lastAlertOutput.write("The last alert of "+ date + '\n')
        lastAlertOutput.write("------------------ " + '\n')

        lastAlertOutput.write("Rule: " + lastAlert["rule"] + '\n')
        lastAlertOutput.write("Level: " + lastAlert["level"] + '\n')
        lastAlertOutput.write("Log file: " + lastAlert["File"] + '\n')
        lastAlertOutput.write("Timestamp: " + str(lastAlert["timestamp"]))
        lastAlertOutput.write('\n')
        lastAlertOutput.close()
		"""
        print("------------------ " + '\n')
        print("The last alert of "+ date + '\n')
        print("Rule: " + lastAlert["rule"] + '\n')
        print("Level: " + lastAlert["level"] + '\n')
        print("Log file: " + lastAlert["File"] + '\n')
        print("Timestamp: " + str(lastAlert["timestamp"]))
        print('\n')
		
if __name__ == "__main__":
	main(sys.argv[1:])

