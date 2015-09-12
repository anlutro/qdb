(function() {
	function makeHttpRequest(method, url, data, callback)
	{
		var req = new XMLHttpRequest();
		req.onreadystatechange = callback;
		req.open(method, url, true);
		req.send(data);
	}

	function removeElementById(id)
	{
		var e = document.getElementById(id);
		e.parentElement.removeChild(e);
	}

	function decrementPendingCounter()
	{
		var e = document.getElementById('pending-count');
		if (!e) {
			return;
		}
		e.innerText = parseInt(e.innerText) - 1;
	}

	function approveQuote()
	{
		var quoteId = this.dataset.quoteId;
		var url = '/'+quoteId+'/approve';
		makeHttpRequest('POST', url, null, function() {
			if (this.readyState === 4 && this.status === 200) {
				alert('Quote approved!');
				decrementPendingCounter();
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
		makeHttpRequest('DELETE', url, null, function() {
			if (this.readyState === 4 && this.status === 200) {
				alert('Quote deleted!');
				removeElementById('quote-'+quoteId);
			}
		});
	}

	function editQuote()
	{
		var quoteId = this.dataset.quoteId;
		var quoteEl = document.getElementById('quote-'+quoteId);
		var bodyEl = quoteEl.getElementsByClassName('quote-body')[0];
		bodyEl.classList.add('hidden');
		var inputEl = quoteEl.getElementsByClassName('quote-edit')[0];
		inputEl.classList.remove('hidden');
	}

	function cancelEditQuote()
	{
		var quoteId = this.dataset.quoteId;
		var quoteEl = document.getElementById('quote-'+quoteId);
		var bodyEl = quoteEl.getElementsByClassName('quote-body')[0];
		bodyEl.classList.remove('hidden');
		var editEl = quoteEl.getElementsByClassName('quote-edit')[0];
		editEl.classList.add('hidden');
	}

	function submitEditQuote()
	{
		var quoteId = this.dataset.quoteId;
		var url = '/'+quoteId;
		var quoteEl = document.getElementById('quote-'+quoteId);
		var formEl = quoteEl.getElementsByClassName('quote-edit')[0];
		var inputEl = quoteEl.getElementsByClassName('quote-edit-input')[0];
		makeHttpRequest('PATCH', url, new FormData(formEl), function() {
			if (this.readyState === 4 && this.status === 200) {
				alert('Quote updated!');
				location.reload();
			}
		});
	}

	function addClickListener(className, listenerFunc)
	{
		var elements = document.getElementsByClassName(className);

		for (var i = elements.length - 1; i >= 0; i--) {
			elements[i].addEventListener('click', listenerFunc, false);
		}
	}

	addClickListener('quote-approve_button', approveQuote);
	addClickListener('quote-delete_button', deleteQuote);
	addClickListener('quote-edit_button', editQuote);
	addClickListener('quote-edit-submit_button', submitEditQuote);
	addClickListener('quote-edit-cancel_button', cancelEditQuote);
})();
