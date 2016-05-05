import unittest
import datetime

from qdb.models import Quote


def make_quote(body='', submitted_at=None, submitter_ip=None, approved=False):
	if not submitted_at:
		submitted_at = datetime.datetime.now()
	return Quote(body, submitted_at, submitter_ip, approved)


class QuoteTest(unittest.TestCase):
	def test_submitted_at_print_is_correct_type(self):
		dt = datetime.datetime(2015, 1, 1, 12, 0, 0)
		quote = make_quote(submitted_at=dt)
		self.assertIsInstance(quote.submitted_at_print, datetime.datetime)

		dt = datetime.datetime(2015, 1, 1, 0, 0, 0)
		quote = make_quote(submitted_at=dt)
		self.assertNotIsInstance(quote.submitted_at_print, datetime.datetime)
		self.assertIsInstance(quote.submitted_at_print, datetime.date)

	def test_prepare_strips_timestamp(self):
		text = '[01:23] <asdf> foobar\n[01:23]  * asdf stuff'
		self.assertEqual(text, Quote.prepare(text, strip_timestamps=False))

		expected = '<asdf> foobar\n* asdf stuff'
		self.assertEqual(expected, Quote.prepare(text))

	def test_strips_voice_and_ops(self):
		text = '<+Abc> a\n<@dEf> b\n< ghJ> c'
		expected = '<Abc> a\n<dEf> b\n<ghJ> c'
		self.assertEqual(expected, Quote.prepare(text))
