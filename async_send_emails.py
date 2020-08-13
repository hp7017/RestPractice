import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'RestPractice.settings'
django.setup()

from django.core.mail import EmailMessage, get_connection
from LibGen import models
while True:
	if models.Email.objects.exists():
		emails = models.Email.objects.all()
		emails_for_connection = []
		connection = get_connection()
		connection.open()
		for email in emails:
			email_message = EmailMessage(
				subject=email.subject,
				body=email.body,
				from_email=email.from_email,
				to=[email.to_email],
				reply_to=[email.reply_to]
			)
			emails_for_connection.append(email_message)
			print(f'sent from: {email.from_email}\tto:{[email.to_email]}')
			email.delete()
		connection.send_messages(emails)
		connection.close()