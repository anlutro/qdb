import math

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
from flask.json import JSONEncoder
import qdb.models


def is_spam(text):
    likelyhood = sum(text.count(s) for s in ("<a href", "[url", "[link"))

    return likelyhood > 2


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, qdb.models.Quote):
            return obj.to_json_dict()
        if isinstance(obj, Paginator):
            return {
                "items": obj.items,
                "current_page": obj.page,
                "total_count": obj.total_count,
                "per_page": obj.per_page,
                "total_pages": obj.last_page,
            }
        return super(CustomJSONEncoder, self).default(obj)


class Paginator:
    per_page = 50
    page_qs = "p"

    def __init__(self, query, page, url):
        self.total_count = query.count()
        page = int(page)
        if page > 1:
            query = query.offset(self.per_page * (page - 1))
        self.items = query.limit(self.per_page).all()
        self.page = page
        self.url = url
        self.last_page = math.ceil(self.total_count / self.per_page)
        self.pages = range(1, int(self.last_page) + 1)
        self._html = None

    def __str__(self):
        return self.html

    @property
    def html(self):
        if self._html is None:
            self._html = self._render_html()
        return self._html

    def _render_html(self):
        # parse the url outside of the gen_page_link function for efficiency
        scheme, host, path, qs, fragment = urlparse.urlsplit(self.url)
        query_params = urlparse.parse_qs(qs)

        # this function will replace the page query string in an url to match
        # the page, create an <a> element, and add the "active" class to it if
        # it corresponds to the currently active page.
        def gen_page_link(page):
            query_params[self.page_qs] = [page]
            new_query_string = urlparse.urlencode(query_params, doseq=True)
            link = urlparse.urlunsplit((scheme, host, path, new_query_string, ""))
            link_class = ""
            if self.page == page:
                link_class = "active"
            return '<a href="{}" class="{}">{}</a>'.format(link, link_class, page)

        pages_html = "".join([gen_page_link(page) for page in self.pages])

        # figure out the range of items we're currently browsing
        start = self.per_page * (self.page - 1) + 1
        end = min(self.page * self.per_page, self.total_count)
        if start == end:
            item_range = start
        else:
            item_range = str(start) + "-" + str(end)

        html = (
            '<div class="range">Showing #{} out of {} quotes</div>'
            '<div class="pages">{}</div>'
        )
        return html.format(item_range, self.total_count, pages_html)
