from qdb.format import *


def test_prepare_strip_timestamp():
	text = '[01:23] <asdf> foobar\n[01:23]  * asdf stuff'
	expected = '<asdf> foobar\n* asdf stuff'
	assert expected == strip_timestamps(text)


def test_strip_modes():
	text = '<+Abc> a\n<@dEf> b\n< ghJ> c'
	expected = '<Abc> a\n<dEf> b\n<ghJ> c'
	assert expected == strip_modes(text)


def test_normalize_nick_format():
	text = '+asdf123 | foobar\n ghjk987 | barbaz'
	expected = '<asdf123> foobar\n<ghjk987> barbaz'
	assert expected == normalize_nick_format(text)
