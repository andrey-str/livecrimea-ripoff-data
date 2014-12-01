import urllib2
import urllib

import re
from collections import OrderedDict
import os
import shutil
from BeautifulSoup import BeautifulSoup

import socket


def mkOutDir(directory, deleteIfExists=True):
	exists = os.path.exists(directory)

	if(exists and deleteIfExists):
		shutil.rmtree(directory);
		exists = False;

	if(not exists):
		os.mkdir(directory);

def getImageLocations(html):
	# (?<=...) means "Matches if the current position in the string 
	#                 is preceded by a match for ... 
	#                 that ends at the current position."
	loc = re.findall('(?<=IMG SRC=")image/\d+/[\w\d_]+.jpg', html)
	return loc

def getListOfUrls():

	pattern = '"/node/\d\d\d\d*">';
	prog = re.compile(pattern);

	exlude_patterns = ('"/node/1476"', '/node/4515', '<span class="field-content"><a href="/node/\d*"', '/node/\d*#comment-')
	exlude_progs = list()

	for ex in exlude_patterns:
		exlude_progs.append(re.compile(ex));
		pass

	nodes.extend(["/node/1476", "/kayak"]);

	for x in xrange(0,51): #51 actuall :-)

		url = "http://livecrimea.com/all/3?page=" + str(x)
		print url

		response = urllib2.urlopen(url);
		html = response.read();

		#print html
		if True:
			i = 0
			for ex_p in exlude_progs:
				print "Iteration of remove trashy records #" + str(i) + " ..."
				matches = ex_p.findall(html)
			
				#print matches

				for m in matches:
					html = html.replace(m,"")
					pass

				i = i + 1;

		
		print "Real search"
		matches = prog.findall(html)

		ordered_list = list(OrderedDict.fromkeys(matches));
		ordered_list = [w.replace('>','') for w in ordered_list]
		ordered_list = [w.replace('"','') for w in ordered_list]
		nodes.extend(ordered_list)

		pass

	print nodes

	print "Total nodes: " + str(len(nodes));

def downloadImagesFromHtml(html):
	page = BeautifulSoup(html);

	images_out_dir = "images";
	mkOutDir(images_out_dir, False);
	os.chdir(images_out_dir);

	e_p = 'korj2korj.users.photofile.ru';
	e_pr = re.compile(e_p);

	
	for img in page.findAll('img'):
		try:
			img_url = img['src'];

			m = e_pr.findall(img_url)

			if(not m):

				local_img_name = os.path.abspath(img_url.split('/')[-1]);

				if not os.path.exists(local_img_name):
					print "Downloading " + img_url + " to " + local_img_name;
					try:
						urllib.urlretrieve(img_url, local_img_name);
					except:
						print "Can't download " + img_url
						pass
				else:
					print "File exists";
					pass
		except:
			print "Probably incorrect img tag: " + str(img);
			pass;


	

########

#socket.setdefaulttimeout(1)

wd = os.path.dirname(os.path.realpath(__file__))
out_dir = "out"
nodes = list();

mkOutDir(out_dir, False)

os.chdir(os.path.join(wd, out_dir))

getListOfUrls()

for x in nodes:
	os.chdir(os.path.join(wd, out_dir))
	url = "http://livecrimea.com/" + x;
	print url;

	folder_name = url.split('/')[-1];

	mkOutDir(folder_name, False)
	os.chdir(os.path.join(wd, out_dir, folder_name))
	try:
		response = urllib2.urlopen(url);
		html = response.read();

		if not os.path.exists(folder_name + ".html"):
			with open(folder_name + ".html", "w") as text_file:
				text_file.write(html)

		downloadImagesFromHtml(html);

	except:
		print "Probably access denied for url: " + str(url);
		pass;

print "done";
# for x in nodes:

# 	url = "http://livecrimea.com/" + x;

# 	print url;

# 	response = urllib2.urlopen(url);
# 	html = response.read();

# 	pass

