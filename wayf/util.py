import re 

def urldecode(string):
    urlenc = re.compile(r'%([0-9a-fA-F]{2})')
    return urlenc.sub(lambda x: chr(int(x.group(1), 16)), string)
