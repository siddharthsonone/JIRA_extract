import re
import os
import time
import datetime as dt
from jira.client import JIRA
from tqdm import tqdm
import pymssql
import json

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

ip_query = '''
project = "Technical Operations Service Desk" 
AND Key in ('TOSD-90183', 'TOSD-92931', 'TOSD-92818', 'TOSD-90654')

'''
scope_tickets = jira.search_issues(ip_query,
                                   startAt=0, maxResults=400, 
                                   validate_query=True,  expand='changelog', json_result=None)
insert_date = dt.datetime.now().date()
bad=[]
for ticket in tqdm(scope_tickets):
    
    if ('Brandon' in ticket.fields.creator.displayName) and  ('Professional' in ticket.fields.summary) or ('Synchronization ' in ticket.fields.summary):
        print 'Addon'
        changelog = ticket.changelog
        t_uptime = []
        entry = []
        for history in changelog.histories:
            
            for item in history.items:
            
                if item.field == 'status':
                    
                    entry = ((ticket), #Ticket
                                (ticket.fields.summary).encode('ascii','ignore').replace("'",""), #Summary
                                ticket.fields.creator.displayName.encode('ascii','ignore'), #Creator
                                dt.datetime.strptime((history.created.replace('T', ' ').split('.')[0]),date_format), #DateTime Object
                                item.fromString.encode('ascii','ignore'), #from
                                item.toString.encode('ascii','ignore'),  #to
                                (history.author.displayName).encode('ascii','ignore'), #Handeld By
                                insert_date)
                    t_uptime.append(entry) 
                    
        while len(t_uptime) > 1:
            
            print t_uptime[0][0], t_uptime[0][1], t_uptime[0][2], t_uptime[0][3], t_uptime[0][4], t_uptime[0][5], t_uptime[0][6], (t_uptime[1][3] - t_uptime[0][3]),t_uptime[0][7]
                                           
            cursor_.execute( '''INSERT INTO JIRA_Dump_Uptime ([TICKET ID], [Summary], [Creator],  [DateTime] ,[Status From], [Status To], [Assignee], [Time Spent],[InsertDate]) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (t_uptime[0][0], t_uptime[0][1]
                                , t_uptime[0][2], t_uptime[0][3]
                                , t_uptime[0][4], t_uptime[0][5]
                                , t_uptime[0][6], (t_uptime[1][3] - t_uptime[0][3]),t_uptime[0][7]))
            t_uptime.pop()
        connec.commit() 
        

    elif 'tosd.addon' in ticket.fields.labels: #Addons
        print 'Uptime' 
                    
        changelog = ticket.changelog
        t_addon = []

        for history in changelog.histories:
            
            for item in history.items:
                
                if item.field == 'status':
                    
                    addon_entry = (
                                str(ticket).encode('ascii', 'ignore') #Ticket
                                ,((ticket.fields.summary)).replace("'","").replace(u"\u2018", "").replace(u"\u2019", "").encode('ascii', 'ignore') #Summary
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
                    t_addon.append(addon_entry)
                   
        while len(t_addon) > 1:
            
            print t_addon[0][0], t_addon[0][1], t_addon[0][2], t_addon[0][3], t_addon[0][4], t_addon[0][5], t_addon[0][6], t_addon[0][7], t_addon[0][8], t_addon[0][9], t_addon[0][10], (t_addon[1][7] - t_addon[0][7]) 
            
            cursor_.execute( '''INSERT INTO JIRA_dump ([TICKET ID], [Summary], [Submitter], [PMS], [Quantity], [Zocdoc ProviderID], [Due Date], [DateTime] ,[Assignee], [Status From], [Status To],[Time Spent]) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (t_addon[0][0], t_addon[0][1], t_addon[0][2], t_addon[0][3]
                , t_addon[0][4], t_addon[0][5], t_addon[0][6], t_addon[0][7]
                , t_addon[0][8], t_addon[0][9], t_addon[0][10], (t_addon[1][7] - t_addon[0][7])))
                
            t_addon.pop(0)
        connec.commit() 

    elif 'TO' in ticket.fields.summary:
        #Implementation Mapping Module
        pass 
       





