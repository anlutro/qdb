#!/usr/bin/env python3

import re

class Quote:
	def __init__(self, timestamp, body):
		self.timestamp = timestamp
		self.body = body

def extract_quote(body):
	parts = body.split('\'')
	timestamp = int(parts[0].split(',')[1].strip())
	body = '\''.join(parts[3:])
	end = body.rfind('\'')
	body = body[:end]
	body = body.replace('\'\'', '\'')
	body = body.replace('\\r\\n', '\n')
	body = body.replace('\\n', '\n')
	body = body.replace('\\r', '\n')

	expr = re.compile(r'^[\[\(]?\d{1,2}\:?\d{2}(\:?\d{2})?(\s*(AM|PM))?[\]\)]?\s*')
	lines = []
	for line in body.split('\n'):
		lines.append(expr.sub('', line))
	body = '\n'.join(lines)
	body = re.sub(r'\s{2,}', ' ', body)
	body = body.strip()

	return Quote(timestamp, body)

def extract_quotes(path):
	quotes = []
	with open(path, 'r') as f:
		contents = f.read()
	for line in contents.split('\n'):
		quotes.append(extract_quote(line))
	return quotes

def generate_pgsql(quotes):
	for quote in quotes:
		body = quote.body.replace('\'', '\\\'').replace('\n', '\\n')
		print('INSERT INTO quotes (submitted_at, body, score, approved) VALUES (to_timestamp({}), E\'{}\', 0, true);'.format(
			quote.timestamp, body))

def main():
	quotes = extract_quotes('mysql_dump.txt')
	generate_pgsql(quotes)
if __name__ == '__main__':
	main()
