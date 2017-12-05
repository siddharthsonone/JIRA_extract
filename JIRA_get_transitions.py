import re
import os
import time
import json
import datetime as dt
from jira.client import JIRA
import pymssql

creds = json.load(open(r'C:\Users\siddharth.sonone\Desktop\JIRA\cred.json'))


server = creds["db_server"]
usrname = creds["db_username"]
password = creds["db_password"]
db = creds["db_name"]

connec = pymssql.connect(server, usrname, password, db)
cursor_ =  connec.cursor()

date_format = "%Y-%m-%d %H:%M:%S"

options = creds["server"]
jira = JIRA(options, basic_auth=(creds["username"], creds["password"]))

ip_query = '''project = "Technical Operations Service Desk" and labels = 'tosd.addon' and createdDate > endOfWeek(-2)'''
scope_tickets = jira.search_issues(ip_query,
                                   startAt=0, maxResults=50, 
                                   validate_query=True,  expand='changelog', json_result=None)

#get the list of Entries
print 'The total number of tickets are {%d}'%len(scope_tickets) 
bad_tickets = []
for ticket in scope_tickets:
    
    changelog = ticket.changelog
    transitions = []
    for history in changelog.histories:
        for item in history.items:
            if item.field == 'status':
                print str(ticket).encode('ascii', 'ignore'),(ticket.fields.summary).encode('ascii', 'ignore'),str(ticket.fields.creator).encode('ascii', 'ignore'),str(ticket.fields.customfield_11406).encode('ascii', 'ignore'),str(ticket.fields.customfield_13506).encode('ascii', 'ignore'),str(ticket.fields.customfield_14100).encode('ascii', 'ignore'),(ticket.fields.duedate).encode('ascii', 'ignore'),dt.datetime.strptime((history.created.replace('T', ' ').split('.')[0]),date_format),(history.author.displayName).encode('ascii', 'ignore'),item.fromString,item.toString
                #get transitions in a list
                entry =[(str(ticket).encode('ascii', 'ignore') #Ticket
                ,str(ticket.fields.summary).encode('ascii', 'ignore') #Summary
                ,str(ticket.fields.creator).encode('ascii', 'ignore') #Creator 
                ,str(ticket.fields.customfield_11406).encode('ascii', 'ignore') #PMS
                ,str(ticket.fields.customfield_13506).encode('ascii', 'ignore') #Quantity
                ,str(ticket.fields.customfield_14100).encode('ascii', 'ignore') #ZocdocProviderID
                ,(ticket.fields.duedate).encode('ascii', 'ignore') #DueDate
                ,dt.datetime.strptime((history.created.replace('T', ' ').split('.')[0]),date_format) #TimeStamp
                ,str(history.author.displayName).encode('ascii', 'ignore') #Assignee
                ,item.fromString #fromStatus
                ,item.toString #toStatus
                        )]
                transitions.append(entry)
                #cursor_.execute( "INSERT INTO JIRA_dump ([TICKET ID], [Summary], [Submitter], [PMS], [Quantity], [Zocdoc ProviderID], [Due Date], [DateTime] ,[Assignee], [Status From], [Status To]) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % ( str(ticket).encode('ascii', 'ignore'), str(ticket.fields.summary).encode('ascii', 'ignore'), str(ticket.fields.creator).encode('ascii', 'ignore'),  str(ticket.fields.customfield_11406).encode('ascii', 'ignore'), str(ticket.fields.customfield_13506).encode('ascii', 'ignore'), str(ticket.fields.customfield_14100).encode('ascii', 'ignore'), (ticket.fields.duedate).encode('ascii', 'ignore'), dt.datetime.strptime((history.created.replace('T', ' ').split('.')[0]),date_format), str(history.author.displayName).encode('ascii', 'ignore'), item.fromString, item.fromString))
                
                
                    
connec.commit()
   
        

               
                





