(function() {
	function makeHttpRequest(method, url, callback)
	{
		var req = new XMLHttpRequest();
		req.onreadystatechange = callback;
		req.open(method, url, true);
		req.send(null);
	}

	function removeElementById(id)
	{
		var e = document.getElementById(id);
		e.parentElement.removeChild(e);
	}

	function approveQuote()
	{
		var quoteId = this.dataset.quoteId;
		var url = '/'+quoteId+'/approve';
		makeHttpRequest('POST', url, function() {
			if (this.readyState === 4 && this.status === 200) {
				alert('Quote approved!');
				removeElementById('quote-'+quoteId);
			}
		});
	}

	function deleteQuote()
	{
		if (!window.confirm('Are you sure you want to delete this quote?')) {
			return;
		}
		var quoteId = this.dataset.quoteId;
		var url = '/'+quoteId;
		makeHttpRequest('DELETE', url, function() {
			if (this.readyState === 4 && this.status === 200) {
				alert('Quote deleted!');
				removeElementById('quote-'+quoteId);
			}
		});
	}

	function addClickListener(className, listenerFunc)
	{
		var elements = document.getElementsByClassName(className);

		for (var i = elements.length - 1; i >= 0; i--) {
			elements[i].addEventListener('click', listenerFunc, false);
		};
	}

	addClickListener('quote-approve_button', approveQuote);
	addClickListener('quote-delete_button', deleteQuote);
})();
