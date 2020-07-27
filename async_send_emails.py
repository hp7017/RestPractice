import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'RestPractice.settings'
django.setup()

from django.core.mail import EmailMessage
from LibGen import models
emails = models.Email.objects.all().prefetch_related('to_receivers', 'cc_receivers', 'reply_to')
for email in emails:
	email_message = EmailMessage(
		subject='<subject>',
		body='<body>',
		from_email='himanshupharawal100@gmail.com',
		to=['support@librarygenesis.in'],
		cc=[],
		reply_to=['himanshupharawal100@gmail.com']
	)
	email_message.send(fail_silently=False)