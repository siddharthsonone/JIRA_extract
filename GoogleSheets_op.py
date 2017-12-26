#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime as dt
from jira.client import JIRA
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

user = 'first.last@company.com'

date_format = '%Y-%m-%d %H:%M:%S'
insert_date = dt.datetime.now().date()

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
file_path = r''
creds = ServiceAccountCredentials.from_json_keyfile_name(file_path,
        scope)
client = gspread.authorize(creds)
sheet = client.open('Sample_Sheet')
worksheet = sheet.add_worksheet('%s_Tracker_%s'
                                % (user[:-11].replace('.', ''),
                                insert_date), 300, 12)

options = creds["server"]
jira = JIRA(options, basic_auth=(creds["username"], creds["password"]))

ip_query = \
    '''
project = tosd 
and assignee 
was '%s'
and updatedDate > startOfDay() 
and updatedDate < endOfDay()
order by updatedDate
''' \
    % user

scope_tickets = jira.search_issues(
    ip_query,
    startAt=0,
    maxResults=400,
    validate_query=True,
    expand='changelog',
    json_result=None,
    )
total_tickets = len(scope_tickets)
row_number = 0
for ticket in scope_tickets:

    changelog = ticket.changelog
    t = []

    for history in changelog.histories:
        for item in history.items:

            if item.field == 'status':

                lambda entry: (entry.encode('ascii,ignore'
                               ) if type(entry) == 'str' else entry)
                entry = map(lambda entry: (entry.encode('ascii,ignore'
                            ) if type(entry) == 'str' else entry), [
                    ticket,
                    ticket.fields.summary.replace("'", '').replace("Professional Locked - ", '').replace("Synchronization Down for SyncId ", ''),
                    ticket.fields.creator.displayName,
                    dt.datetime.strptime(history.created.replace('T',
                            ' ').split('.')[0], date_format),
                    item.fromString,
                    item.toString,
                    history.author.displayName,
                    ])
                t.append(entry)

    while len(t) >= 1:

        if len(t) == 1:
            row_number += 1
            worksheet.update_cell(row_number, 1, t[0][0])
            worksheet.update_cell(row_number, 2, t[0][1])
            worksheet.update_cell(row_number, 3, t[0][2])
            worksheet.update_cell(row_number, 4, t[0][3])
            worksheet.update_cell(row_number, 5, t[0][4])
            worksheet.update_cell(row_number, 6, t[0][5])
            worksheet.update_cell(row_number, 7, t[0][3] - t[0][3])
            t.pop(0)
        else:

            row_number += 1
            worksheet.update_cell(row_number, 1, t[0][0])
            worksheet.update_cell(row_number, 2, t[0][1])
            worksheet.update_cell(row_number, 3, t[0][2])
            worksheet.update_cell(row_number, 4, t[0][3])
            worksheet.update_cell(row_number, 5, t[0][4])
            worksheet.update_cell(row_number, 6, t[0][5])
            worksheet.update_cell(row_number, 7, t[1][3] - t[0][3])

            t.pop(0)
			
