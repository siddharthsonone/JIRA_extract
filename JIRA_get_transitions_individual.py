import os
import time
import json
import datetime as dt
from jira.client import JIRA

creds = json.load(open(r'C:\Users\siddharth.sonone\Desktop\JIRA\cred.json'))


date_format = "%Y-%m-%d %H:%M:%S"

options = creds["server"]
jira = JIRA(options, basic_auth=(creds["username"], creds["password"]))



ticket_ = 'TOSD-92543'

try:
	ticket = jira.issue(ticket_, expand='changelog')


	changelog = ticket.changelog
	transitions = []
	for history in changelog.histories:
	   
	    for item in history.items:
	        
	        if item.field == 'status':
	            
	            
	            #get transitions in a list
	            entry  =[((ticket) 
	                    ,dt.datetime.strptime((history.created.replace('T', ' ').split('.')[0]),date_format)
	                    ,(history.author.displayName).encode('ascii', 'ignore'))
	                    ,item.fromString, item.toString]
	            transitions.append(entry)
	            
	#TextReport
	times_differences=[]
	while len(transitions)>1:
	    
	    delta = transitions[1][0][1] - transitions[0][0][1] 
	    print str(transitions[0][0][0]) + ' on ' +str(transitions[0][0][1]) + ' was actioned by ' + str(transitions[0][0][2]) + ' making transition :- ' + str(transitions[0][1]) + ' to ' + str(transitions[0][2])
	    transitions.pop(0)
	    print 'After ' +str(delta) + '\n'
	    times_differences.append(delta)
	    #print len(transitions)
	    #print len(times_differences)
	    #print '\n'        

	#print 'Done'
	#print times_differences    
	temp=[]
	for t in times_differences:
	    pass
	    #print t
except:
	print 'Bad infor %s' % ticket_
