import json
import urllib.request

from qdb import app


def notify_bot(quote):
	data = {'quote': quote.to_json_dict()}
	body = json.dumps(data).encode('utf-8')
	url = app.config.get('IRCBOT_WEBHOOK_URL')

	urllib.request.urlopen(url, body, timeout=1)
