import math
import re
import urllib

class Paginator:
	per_page = 50
	page_qs = 'p'

	def __init__(self, query, page, url):
		self.total_count = query.count()
		page = int(page)
		if page > 1:
			query = query.offset(self.per_page * (page - 1))
		self.items = query.limit(self.per_page).all()
		self.page = page
		self.url = url
		self.last_page = math.ceil(self.total_count / self.per_page)
		self.pages = range(1, self.last_page + 1)
		self.html = self._render_html()

	def __str__(self):
		return self.html

	def _render_html(self):
		# parse the url outside of the gen_page_link function for efficiency
		scheme, host, path, qs, fragment = urllib.parse.urlsplit(self.url)
		query_params = urllib.parse.parse_qs(qs)

		# this function will replace the page query string in an url to match
		# the page, create an <a> element, and add the "active" class to it if
		# it corresponds to the currently active page.
		def gen_page_link(page):
			query_params[self.page_qs] = [page]
			new_query_string = urllib.parse.urlencode(query_params, doseq=True)
			link = urllib.parse.urlunsplit((scheme, host, path, new_query_string, ''))
			link_class = ''
			if self.page == page:
				link_class = 'active'
			return '<a href="{}" class="{}">{}</a>'.format(link, link_class, page)
		pages_html = ''.join([gen_page_link(page) for page in self.pages])

		# figure out the range of items we're currently browsing
		start = self.per_page * (self.page - 1) + 1
		end = min(self.page * self.per_page, self.total_count)
		if start == end:
			item_range = start
		else:
			item_range = str(start)+'-'+str(end)

		return ('<div class="range">Showing #{} out of {} quotes</div>' + \
			'<div class="pages">{}</div>').format(item_range, self.total_count, pages_html)
