import re 
from datetime import datetime as dt


console.clear()
log_text = editor.getText()

op=''
results=[]
keywords = ['AppointmentId','Procedure', 'StartTime', 'BookedOn','LocationId', 'DurationInMinutes', 'AssistantId', 'ProfessionalId']

console.show()

try:
	
	for key in keywords:
	
		search_query = r'\d+\/\d{2}\/\d{4}\s+\d+:\d{2}:\d{2}\s+[A-Z][A-Z]:\s+\W{1}\s+(%s\s{1}.*)\s+' %key
		results.append(re.search(search_query, log_text).group(1))
		console.write(results[-1] + '\n')
		
		
except:
		console.write('Regex failed or something weird happened')
		

op = ' '.join(str(result) for result in results)

booked_date =  re.search(r'\d+/\d{2}/\d{4}\s{1}\d+:\d{2}:\d{2}\s+[A-Z][A-Z]:\s+\S{1}\s+BookedOn\s+-\s{1}(.*)\s\w+\s+', log_text).group(1).strip()
appointment_date =  re.search(r'\d+/\d{2}/\d{4}\s{1}\d+:\d{2}:\d{2}\s+[A-Z][A-Z]:\s+\S{1}\s+StartTime\s+-\s{1}(.*)\s\w+\s+', log_text).group(1).strip()
cnvr = lambda date_str : dt.strptime(date_str ,'%m/%d/%Y %H:%M:%S') 
console.write('Appointment was boooked '+str(cnvr(appointment_date)-cnvr(booked_date))+ ' hours ago in advance')

