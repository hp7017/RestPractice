# import os
# import django
# os.environ['DJANGO_SETTINGS_MODULE'] = 'RestPractice.settings'
# django.setup()

# from django.core.mail import EmailMessage
# from LibGen import models
# while True:
# 	if models.Email.objects.exists():
# 		emails = models.Email.objects.all()
# 		for email in emails:
# 			email_message = EmailMessage(
# 				subject=email.subject,
# 				body=email.body,
# 				from_email=email.from_email,
# 				to=[email.to_email],
# 				reply_to=[email.reply_to]
# 			)
# 			print(f'sent from: {email.from_email}\tto:{[email.to_email]}')
# 			email_message.send(fail_silently=False)
# 			email.delete()
import requests
from bs4 import BeautifulSoup
import json
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)
r = requests.get('https://free-proxy-list.net/')
bsobj = BeautifulSoup(r.text)
proxies = ['{0}:{1}'.format(tr.findAll('td')[0].get_text(), tr.findAll('td')[1].get_text()) for tr in bsobj.find('tbody').findAll('tr') if tr.findAll('td')[6].get_text() == 'no']
file = open(os.path.join(base_dir, 'proxies.json'), 'w')
file.write(json.dumps(proxies))
# from collections import OrderedDict

# This data was created by using the curl method explained above
# headers_list = [
#     # Firefox 77 Mac
#      {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Referer": "https://www.google.com/",
#         "DNT": "1",
#         "Connection": "keep-alive",
#         "Upgrade-Insecure-Requests": "1"
#     },
#     # Firefox 77 Windows
#     {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Referer": "https://www.google.com/",
#         "DNT": "1",
#         "Connection": "keep-alive",
#         "Upgrade-Insecure-Requests": "1"
#     },
#     # Chrome 83 Mac
#     {
#         "Connection": "keep-alive",
#         "DNT": "1",
#         "Upgrade-Insecure-Requests": "1",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "Sec-Fetch-Site": "none",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Dest": "document",
#         "Referer": "https://www.google.com/",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
#     },
#     # Chrome 83 Windows 
#     {
#         "Connection": "keep-alive",
#         "Upgrade-Insecure-Requests": "1",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "Sec-Fetch-Site": "same-origin",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-User": "?1",
#         "Sec-Fetch-Dest": "document",
#         "Referer": "https://www.google.com/",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "en-US,en;q=0.9"
#     }
# ]
# # Create ordered dict from Headers above
# import json
# ordered_headers_list = []
# for headers in headers_list:
#     h = OrderedDict()
#     for header,value in headers.items():
#         h[header]=value
#     ordered_headers_list.append(h)
# f = open('headers.json', 'w')
# f.write(json.dumps(ordered_headers_list))
# f.close()