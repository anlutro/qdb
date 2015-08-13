from sqlalchemy import Column, Integer, Text, DateTime, Boolean
from qdb.database import Base
import re
import datetime

class Quote(Base):
	__tablename__ = 'quotes'

	id = Column(Integer, primary_key=True)
	body = Column(Text)
	submitted_at = Column(DateTime)
	approved = Column(Boolean)
	score = Column(Integer)

	def __init__(self, body, submitted_at, score=0, approved=False):
		self.body = body
		self.submitted_at = submitted_at
		self.approved = approved
		self.score = score

	@property
	def submitted_at_print(self):
		dt = self.submitted_at
		if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
			return datetime.date(dt.year, dt.month, dt.day)
		return dt

	@staticmethod
	def prepare(quote):
		# remove timestamps from the start of each line in the quote
		expr = re.compile(r'^[\[\(]?\d{1,2}\:?\d{2}(\:?\d{2})?(\s*(AM|PM))?[\]\)]?\s*')
		lines = []
		for line in quote.split('\n'):
			lines.append(expr.sub('', line))
		quote = '\n'.join(lines)

		# replace tabs with spaces
		quote = re.sub(r'\t+', ' ', quote)
		# remove windows-style newline characters
		quote = quote.replace('\r', '')

		return quote

	def to_json_dict(self):
		return {
			'id': self.id,
			'body': self.body,
			'submitted_at': self.submitted_at.isoformat(),
			'approved': self.approved,
		}
