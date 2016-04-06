import re
html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;"
	}

def html_escape(text):
	for i in html_escape_table:	
		text = re.sub(html_escape_table[i], i, text)
	return text

f = open("data2.txt","r").readlines()
g = open("data_cleaned.txt", "w")
for i in f:
	if html_escape(i).strip()=="" or (html_escape(i).strip()[0]=="[" and html_escape(i).strip()[-1]==']'):
		continue
	if html_escape(i).strip().split(" ")[-1][0] == '[' and html_escape(i).strip().split(" ")[-1][-1] == ']':
		try:
			times = int(html_escape(i).strip().split(" ")[-1][2:-1])
			for p in range(times):
				g.write(" ".join(html_escape(i).strip().split(" ")[:-1]).strip()+"\n")
		except Exception as E:
			print 2
	else:
			g.write(html_escape(i))

g.close()
