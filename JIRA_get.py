
import re
import os
import time
import datetime as dt
from jira.client import JIRA
from tqdm import tqdm
import pymssql
import json

creds = json.load(open(r'cred.json'))

server = creds["db_server"]
usrname = creds["db_username"]
password = creds["db_password"]
db = creds["db_name"]

connec = pymssql.connect(server, usrname, password, db)
cursor_ =  connec.cursor()

date_format = "%Y-%m-%d %H:%M:%S"

options = creds["server"]
jira = JIRA(options, basic_auth=(creds["username"], creds["password"]))

ip_query = '''project = "Technical Operations Service Desk" and labels = 'tosd.addon' and createdDate > endOfMonth(-2)'''
scope_tickets = jira.search_issues(ip_query,
                                   startAt=0, maxResults=200, 
                                   validate_query=True,  expand='changelog', json_result=None)

#get the list of Entries
print 'The total number of tickets are {%d}'%len(scope_tickets) 
bad_tickets_sql = []
bad_tickets_jira = []
for ticket in tqdm(scope_tickets):
    
    changelog = ticket.changelog
    transitions = []
    entry = []
    for history in changelog.histories:
        
        for item in history.items:
            
            if item.field == 'status':
                #print str(ticket).encode('ascii', 'ignore'),(ticket.fields.summary).encode('ascii', 'ignore'),str(ticket.fields.creator).encode('ascii', 'ignore'),str(ticket.fields.customfield_11406).encode('ascii', 'ignore'),str(ticket.fields.customfield_13506).encode('ascii', 'ignore'),str(ticket.fields.customfield_14100).encode('ascii', 'ignore'),(ticket.fields.duedate).encode('ascii', 'ignore'),dt.datetime.strptime((history.created.replace('T', ' ').split('.')[0]),date_format),(history.author.displayName).encode('ascii', 'ignore'),item.fromString,item.toString
                #get transitions in a list
                
                entry = (
                str(ticket).encode('ascii', 'ignore') #Ticket
                ,(str(ticket.fields.summary)).replace("'","").replace(u"\u2018", "").replace(u"\u2019", "").encode('ascii', 'ignore') #Summary
                ,str(ticket.fields.creator).encode('ascii', 'ignore') #Creator 
                ,(str(ticket.fields.customfield_11406)).replace(u"\u2018", "").replace(u"\u2019", "").replace("'"," ").encode('ascii', 'ignore') #PMS
                ,str(ticket.fields.customfield_13506).encode('ascii', 'ignore') #Quantity
                ,str(ticket.fields.customfield_14100).encode('ascii', 'ignore') #ZocdocProviderID
                ,str(ticket.fields.duedate).encode('ascii', 'ignore') #DueDate
                ,dt.datetime.strptime((history.created.replace('T', ' ').split('.')[0]),date_format) #TimeStamp
                ,(history.author.displayName).replace(u"\u2018", "").replace(u"\u2019", "") #Assignee
                ,(item.fromString) #fromStatus
                ,(item.toString) #toStatus
                            )
                transitions.append(entry)
               
    
    while len(transitions) > 1:
        try:
            cursor_.execute( '''INSERT INTO JIRA_dump ([TICKET ID], [Summary], [Submitter], [PMS], [Quantity], [Zocdoc ProviderID], [Due Date], [DateTime] ,[Assignee], [Status From], [Status To],[Time Spent]) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (transitions[0][0], transitions[0][1], transitions[0][2], transitions[0][3]
                , transitions[0][4], transitions[0][5], transitions[0][6], transitions[0][7]
                , transitions[0][8], transitions[0][9], transitions[0][10], (transitions[1][7] - transitions[0][7])))
            print transitions[0][0], transitions[0][1], transitions[0][2], transitions[0][3], transitions[0][4], transitions[0][5], transitions[0][6], transitions[0][7], transitions[0][8], transitions[0][9], transitions[0][10], (transitions[1][7] - transitions[0][7]) 
            transitions.pop(0)
        except:
            bad_tickets_sql.append(entry)
            print '''INSERT INTO JIRA_dump ([TICKET ID], [Summary], [Submitter], [PMS], [Quantity], [Zocdoc ProviderID], [Due Date], [DateTime] ,[Assignee], [Status From], [Status To],[Time Spent]) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (transitions[0][0], transitions[0][1], transitions[0][2], transitions[0][3]
                , transitions[0][4], transitions[0][5], transitions[0][6], transitions[0][7]
                , transitions[0][8], transitions[0][9], transitions[0][10], (transitions[1][7] - transitions[0][7]))
            continue

    connec.commit()

connec.close()
        

        
       
