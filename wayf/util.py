import re 

def urldecode(string):
    urlenc = re.compile(r'%([0-9a-fA-F]{2})')
    return urlenc.sub(lambda x: chr(int(x.group(1), 16)), string)

def acceptedlangs(http_a_l):
	# "en" is the default language with the lowest weight
	# however, if defined in our input, it'll be overriden
	langs = { 'en': 0 }

	# first construct a dict of lang => weight
	for lang in http_a_l.split(','):
		lang = lang.strip();
		weight = 1

		try:
			(lang, q) = lang.split(';')
			weight = float(q.split('=')[1])
		except ValueError:
			# no weight on that language
			pass

		langs[lang] = weight

		# if language is something like es-BR, also add es
		# down the queue with a weight of 0.1
		if lang.find("-"):
			baselang = lang.split('-')[0]
			if baselang not in langs:
				langs[baselang] = 0.1

	# sort the dict by value and return only the keys back
	sortedlangs = sorted(langs, key=langs.__getitem__, reverse=True)
	return sortedlangs
