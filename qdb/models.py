from sqlalchemy import Column, Integer, Text, DateTime, Boolean
from qdb.database import Base

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
