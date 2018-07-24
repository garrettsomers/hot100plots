## This program is intended to query the Billboard Hot 100 to obtain a new chart.
## It will then format it.

import sys, os
from numpy import loadtxt

def parse_html(date):

	try: lines = open(date+'.html').readlines()
	except IOError:
		'The file doesnt seem to be there'
		quit()

	outlines = []
	grab = False
	first = True
	for line in lines:

		## Add a start and stop.
		if line == 'Current Week\n': grab = True
		if 'Chart Archive Search' in line: grab = False
		if not grab: continue

		## There are lots of random lines we need to throw away.
		## Specify those.
		if   '<div class="chart-number-one__title">' in line:
			line = line.replace('<div class="chart-number-one__title">','')
			line = line.replace('</div>','')
		elif line[0] == '<' or line[0:2] ==  ' <': continue
		elif 'LAST WEEK' in line: continue
		elif 'PEAK POSITION' in line: continue
		elif 'WEEKS ON CHART' in line: continue
		elif line == 'WEEKS AT NO. 1\n': continue
		elif line == '\n' or line == ' \n': continue
		elif line == 'Song Lyrics\n': continue

		## Replace 'current week' with '1', indicating a #1 ranking.
		if line == 'Current Week\n': outlines.append('1\n')
		## Otherwise, save the line.
		else: outlines.append(line)

	## Throw away the irrelevant last line.
	outlines = outlines[:-1]
	## Now combine the data for each song into one line.
	finallines = []
	for i in xrange(len(outlines)):

		if i%3 == 0:
			l1 = outlines[i].strip()
			l2 = outlines[i+1].strip().replace("&#039;","'").replace("&amp;","&")
			l3 = outlines[i+2].strip().replace("&#039;","'").replace("&amp;","&")

			finallines.append(l1+',"'+l2+'","'+l3+'"\n')

	open(date,'w').writelines(finallines)
	return

def get_new_chart(date):
	## Use wget.
	url = 'https://www.billboard.com/charts/hot-100/'
	os.system('wget '+url+date+' -O "'+date+'.html"')
	## Parse the html file.
	parse_html(date)
	## Do you want to delete the html file?
	print 'File parsed. Delete the html original?'
	yorn = raw_input('(y/n) > ')
	if yorn in ('yes','Yes','y','Y'):
		print 'Deleting'
		os.system('rm '+date+'.html')
	else:
		print 'Okay, keeping'
	
	return

if __name__ == '__main__':
	## Check if a single date was passed.
	if len(sys.argv) != 2:
		print "Pass a single date in quotes"
		print "The format is YYYY-MM-DD"
		quit()

	date = str(sys.argv[1])
	get_new_chart(date)

	print date, 'done!'

