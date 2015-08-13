from flask import jsonify
import json
import urllib.request

BASE_URL = 'http://localhost:9123'

def make_post_request(path, quote):
	data = {'quote': quote.to_json_dict()}
	body = json.dumps(data).encode('utf-8')
	url = BASE_URL + path

	urllib.request.urlopen(url, body, timeout=1)

def notify_bot(quote):
	make_post_request('/qdb-update', quote)
