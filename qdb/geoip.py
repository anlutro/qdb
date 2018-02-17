import geoip2.database
import geoip2.errors

city_reader = None
country_reader = None
try:
	city_reader = geoip2.database.Reader('/usr/share/GeoLite2-City.mmdb')
except FileNotFoundError:
	try:
		country_reader = geoip2.database.Reader('/usr/share/GeoLite2-Country.mmdb')
	except FileNotFoundError:
		pass


def get_city_country(ip):
	try:
		if city_reader:
			resp = city_reader.city(ip)
			return (resp.name, resp.country.name)
		elif country_reader:
			return (None, country_reader.country(ip).name)
	except geoip2.errors.AddressNotFoundError:
		pass
	return (None, None)
