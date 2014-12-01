# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import html2text
import os
import codecs
from BeautifulSoup import BeautifulSoup, NavigableString
from safe_html import safe_html, plaintext
import io
import HTMLParser
import markdown2

def strip_tags(html, invalid_tags):
    soup = BeautifulSoup(html)

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""
            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(unicode(c), invalid_tags)
                s += unicode(c)

            tag.replaceWith(s)

    return soup

def strip_comments(html, startComment, endComment):
	html_parts = html.split(startComment)
	html = html_parts[0] + str(html_parts[1].split(endComment)[1])

	return html


def makeMd(html_dir):

	os.chdir(html_dir)

	html_name = html_dir.split("/")[-1] + ".html"

	with io.open (html_name, "r", encoding='utf8') as html_file:
		html = html_file.read().encode('utf-8')

		soup = BeautifulSoup(html);
		#html = strip_tags(html, ["body","head"])
		[s.extract() for s in soup('script')]
		#[s.extract() for s in soup('head')]
		#[s.extract() for s in soup('head')["hidden"]]

		tags = soup.findAll("a", rel="tag")
		title = soup.head.title.contents[0].split("|")[0].strip()

		imgs = soup.findAll("img")
		for img in imgs:
			
			try:
				img["src"] = domainname + "/" + html_name.split(".")[0] + "/images/" + img["src"].split("/")[-1]
			except:
				print "Error while converting image url: " + str(img)
				pass

			pass

		
		[tag.extract() for tag in soup.findAll("ul", { "class" : "links inline" })]

		[item.extract() for item in soup.findAll("div", id="comments")]
		[item.extract() for item in soup.findAll("ul", id="menu2")]
		[item.extract() for item in soup.findAll("div", {"class" : "blockinner"})]
		[item.extract() for item in soup.findAll("a", href='http://karabin.com.ua/top100/index.php')]
		[item.extract() for item in soup.findAll("a", href=re.compile('http://www.vvv.ru/cnt.php3\?id=\d*'))]
		[item.extract() for item in soup.findAll("a", href='http://www.tour.crimea.com/top/')]
	
		html = str(soup);

		html = strip_comments(html, "<!-- Всероссийский рейтинг туристских ресурсов -->", "<!-- /Всероссийский рейтинг туристских ресурсов -->")

		soup = BeautifulSoup(html);

		# remove these tags, complete with contents.
		blacklist = ["script", "style", "head"]

		whitelist = [
		"div", "span", "p", "br", "pre",
		"table", "tbody", "thead", "tr", "td", "a",
		"blockquote",
		"ul", "li", "ol",
		"b", "em", "i", "strong", "u", "font", "img"
		]


		html = safe_html(str(soup), blacklist, whitelist)

		md = html2text.html2text(html)
		md = md.split("[galya](/user/3)", 1)[1]
		md = md.split("Отправить новый комментарий", 1)[0]
		md = md.strip();

		if(len(tags)):
			md = md + "\n\n##### Tags: ";
			firstTag = True
			# preserver tags
			for tag in tags:
				if not firstTag:
					md = md + ", "
				md = md + tag.contents[0]
				firstTag = False
				pass
		
		if len(title):
			md = "# " + title + md;

		if False:
			with open(html_name.split(".")[-2] + ".md", "w") as text_file:
				text_file.write(md)
		else:
			if os.path.exists(html_name.split(".")[-2] + ".md"):
				os.remove(html_name.split(".")[-2] + ".md")

		i = 2

		h = HTMLParser.HTMLParser()
		filename = h.unescape(title)

		while os.path.exists(os.path.join(wd, "out", filename + ".md")):
			filename = title + str(i)
			i = i + 1;

		print filename;
		
		md_html = str(markdown2.markdown(md))
		md_html = '<meta charset="utf-8">\n<html>' + md_html + "</html>"
		with io.open(os.path.join(wd, "out", filename) + ".html", "w",  encoding='utf8') as text_file:
			text_file.write(md_html.decode('utf-8'))

############################################################################################################			
wd = os.path.dirname(os.path.realpath(__file__))

os.chdir(os.path.join(wd, "out"))

domainname = "http://anse.me/livecrimea"

if 1:
	for d in os.listdir(os.path.join(wd, "out")):
		if(os.path.isdir(os.path.join(wd, "out", d))):
			os.chdir(os.path.join(wd, "out"))
			print "Working in " + str(d)
			makeMd(d)
else:
	makeMd("1476")








