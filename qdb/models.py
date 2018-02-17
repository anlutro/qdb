import datetime
from sqlalchemy import Column, Integer, Text, DateTime, Boolean
from qdb.database import Base
from qdb.geoip import get_city_country


class Quote(Base):
	__tablename__ = 'quotes'

	id = Column(Integer, primary_key=True)
	body = Column(Text)
	submitted_at = Column(DateTime)
	submitter_ip = Column(Text)
	approved = Column(Boolean)

	def __init__(self, body, submitted_at, submitter_ip, approved=None):
		self.body = body
		self.submitted_at = submitted_at
		self.submitter_ip = submitter_ip
		self.approved = approved

	@property
	def submitted_at_print(self):
		dt = self.submitted_at
		if (dt.hour == 0 and
		   dt.minute == 0 and
		   dt.second == 0 and
		   dt.microsecond == 0):
			return datetime.date(dt.year, dt.month, dt.day)
		return dt

	@property
	def geoip_info(self):
		city, country = get_city_country(self.submitter_ip)
		if city:
			return '%s, %s' % (city, country)
		elif country:
			return country
		return None

	def to_json_dict(self):
		return {
			'id': self.id,
			'body': self.body,
			'submitted_at': self.submitted_at.isoformat(),
			'approved': self.approved,
		}
