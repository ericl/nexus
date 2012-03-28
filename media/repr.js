/**
 * A representation of navigational state.
 *
 * Repr.deserialize('#serialized_history_state')
 * new Repr(dict)
 * new Repr(dict).serialize()
 */

var DATE_MIN = 100001;
var DATE_MAX = 300001;
var DEFAULT_PAGE = 1;
var DEFAULT_URL = '';
var FS = ',';
var FS2 = '.';

// parse no-hash fallbacks (new tab, new window, etc)
if (location.pathname != "/") {
	var page_match = location.pathname.match(/^\/[0-9]+$/);
	if (page_match)
		DEFAULT_PAGE = page_match.toString().substring(1);
	else {
		DEFAULT_URL = location.pathname;
		if (DEFAULT_URL.charAt(DEFAULT_URL.length-1) == '/')
			DEFAULT_URL = DEFAULT_URL.substring(0, DEFAULT_URL.length-1);
	}
} else if (window.STATIC_COVER)
	DEFAULT_URL = '/cover';

function Repr(dict) {
	this.query = '';
	this.url = '';
	this.page = 0; // differentiate with page=1, which is set when filtering
	this.author = '';
	this.tags = [];
	this.date_min = DATE_MIN;
	this.date_max = DATE_MAX;

	var changed = false;
	if (dict) {
		for (var i in dict) {
			if (this[i] != undefined && this[i] != dict[i])
				changed = true;
			this[i] = dict[i];
		}
	}

	if (!changed)
		this.url = DEFAULT_URL; // sync with real url root

	if (!this.page) {
		if (changed)
			this.page = 1; // filtering - go with first page always
		else
			this.page = DEFAULT_PAGE;
	}

	this.toString = function() {
		return 'Repr Object ' + this.serialize();
	};

	this.isCover = function() {
		return this.serialize() === "#page=1";
	}

	this.serialize = function(nav_attrs_only) {
		var output = [];
		var have_embed = false;
		if (!nav_attrs_only && this.url) {
			output[output.length] = this.url;
			have_embed = true;
		}
		if (this.tags.length > 0)
			output[output.length] = 'tags=' + this.tags.join(FS2);
		if (this.author)
			output[output.length] = 'author=' + this.author;
		if (this.date_min == this.date_max)
			output[output.length] = 'month=' + this.date_min;
		else {
			if (this.date_min != DATE_MIN)
				output[output.length] = 'min=' + this.date_min;
			if (this.date_max != DATE_MAX)
				output[output.length] = 'max=' + this.date_max;
		}
		if (!nav_attrs_only && !have_embed) {
			if (this.query)
				output[output.length] = 'query=' + this.query;
			else if (output.length === 0 || this.page != 1)
				output[output.length] = 'page=' + this.page;
		}
		return '#' + output.join(FS);
	};
}

Repr.deserialize = function(hash) {
	var attrs = {};
	if (hash.charAt(0) == '#')
		hash = hash.substring(1);
	var chunks = hash.split(FS);
	for (var i in chunks) {
		var chunk = chunks[i];
		if (attrs['query'])
			attrs['query'] += ',' + chunk;
		else if (chunk.substring(0,1) == '/')
			attrs['url'] = chunk;
		else if (chunk.substring(0,5) == 'tags=')
			attrs['tags'] = chunk.substring(5).split(FS2);
		else if (chunk.substring(0,7) == 'author=')
			attrs['author'] = chunk.substring(7);
		else if (chunk.substring(0,5) == 'page=')
			attrs['page'] = chunk.substring(5);
		else if (chunk.substring(0,6) == 'month=')
			attrs['date_min'] = attrs['date_max'] = chunk.substring(6);
		else if (chunk.substring(0,4) == 'min=')
			attrs['date_min'] = chunk.substring(4);
		else if (chunk.substring(0,4) == 'max=')
			attrs['date_max'] = chunk.substring(4);
		else if (chunk.substring(0,6) == 'query=')
			attrs['query'] = chunk.substring(6);
	}
	return new Repr(attrs);
};

