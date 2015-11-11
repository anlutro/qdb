import json
from requests import post

from qdb import app


def notify_bot(quote):
	data = {'quote': quote.to_json_dict()}
	body = json.dumps(data).encode('utf-8')
	url = app.config.get('IRCBOT_WEBHOOK_URL')

	post(url, data=body, timeout=1)
