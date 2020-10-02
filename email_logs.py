from RestPractice import env
from django.core.mail import EmailMessage
import requests
from datetime import datetime
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'RestPractice.settings'
django.setup()
username = env.USERNAME
token = env.TOKEN
paths = ['var/log/www.librarygenesis.in.server.log', 'var/log/www.librarygenesis.in.error.log']
for path in paths:
	r = requests.get(f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path/{path}', headers={'Authorization': 'Token {token}'.format(token=token)})
	date = datetime.now()
	date = date.strftime('%Y-%m-%d')
	lines = r.text.split('\n')
	today_lines = [line for line in lines if line.split(' ')[0] == date]
	today_data = '\n'.join(today_lines)
	email = EmailMessage(
		from_email='Django Server <server@librarygenesis.in>',
		to=['himanshu.pharawal@librarygenesis.in'],
		subject=f'Server Logs [{date}]',
		body=f'{today_data}')
	email.send(fail_silently=False)