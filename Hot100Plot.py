from numpy import *
from datetime import date, timedelta
import matplotlib
import matplotlib.pyplot as pl 
import sys, os

instructions = '''
This program produces a plot of the chart locations of every song by 
a specified artist on the Billboard Hot 100 chart since it's inception
in 1958. This program can be called in one of two ways.

1) Pass two arguments.
	artist_name (str) = The name of the band/artist. If the name contains a space, put it in quotes.
	top_x       (int) = Only consider chartings within the top X. I.E. top 100, top 50, top 10, etc.

	example: python Hot100Plot.py "Taylor Swift" 100
	
	![Tay-tay](https://github.com/garrettsomers/hot100plots/blob/master/TaylorSwift_100.png)

2) Pass four arguments.
	artist_name (str) = Same as above.
	top_x       (int) = Same as above.
	ForceYr1    (int) = Force the chart to begin on Jan 1 of a specified year.
	ForceYr2    (int) = Force the chart to end on Dec 31 of a specified year.

	example: python Hot100Plot.py Madonna 50 1983 2004
	
	![My lady](https://github.com/garrettsomers/hot100plots/blob/master/Madonna_50_1983_2005.png)


Notes of caution:
	If the string of text used for the artist name is contained within another artist name,
	those songs will also be recorded. For example if the artist_name is "Micheal", it will
	produce a plot show songs from Michael Jackson, Michael McDonald, George Michael, etc.

	A song will be collect if artist_name is either a lead artist or featured artist.

	If a singer charts a ton of songs at the same time, as currently coded the names will
	all lie on top of each other (try Drake...lol...). This seems like a pain to fix so
	I will probably just leave it as is. 

	There may be some wonkiness with respect to band names with special characters in them,
	like ' " &. These are probably fixable, but all the problems won't be enounctered for
	some time I am sure.
'''

def artist_plot(artist_name,top_x,*args):

	## Check if we are forcing the plot to begin and end with certain years.
	if   len(args) == 0: ForceYears = False
	elif len(args) == 2: ForceYears, ForceYr1, ForceYr2 = True, args[0], args[1]
	else:
		print 'There must be either 2 or 4 arguments passed.'
		quit()

	## Create a list of colors to iterate through.
	AllColors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#6a3d9a','#fdbf6f','#ff7f00','#cab2d6','#e31a1c','gold','#b15928','k']
	## Read in all the dates of Hot 100 lists.
	dates = sorted(os.listdir('hot100charts/'))
	allsongs = []
	## Cycle through every list searching for artist_name.
	for day in dates:
		lines = open('hot100charts/'+day).readlines()
		for i in xrange(len(lines)):
			line = lines[i]
			rank   = line.rsplit(',')[0]
			song   = line.rsplit(',')[1].replace('"','')
			artist = line.rsplit(',')[2].replace('"','')
			if artist_name in artist:
				## Found the artists name! Make sure its above our cutoff.
				if int(rank) > int(top_x): continue
				## Create a vector for dates and rankings for this song.
				try: vars()[song]
				except KeyError:
					vars()[song] = []
				## Save the date and ranking.
				vars()[song].append([day,int(rank)])
				if song not in allsongs: allsongs.append(song)

	## Save a vector of every date from start to end. The index of each date
	## in the vector will correspond to where the lines are plotted.
	d1 = date(1958, 1, 1)  # start date
	d2 = date(2019, 1, 1)  # end date
	delta = d2 - d1         # timedelta
	outdates = []
	for i in range(delta.days + 1):
		## Save the dates.
		outdates.append(str(d1 + timedelta(i)))

	## Make the figure.
	fig1 = pl.figure(figsize=(15,5))
	ax11 = fig1.add_subplot(111)

	## Set the y-axis locations for plotting song names.
	spacing = logspace(log10(0.15),log10(0.9),13)

	## Go through each song and find the dates since the start corresponding to each chart week.
	## Also, save the first and last dates to set the x axis later.
	FirstDay, LastDay = [], []
	for i, song in enumerate(allsongs):
		## Grab the dates and ranks for this song, and the corresponding index for each date.
		stuff = vars()[song]
		songdates, songranks = zip(*stuff)
		songnums = [outdates.index(sd) for sd in songdates]
		## Get the next color.
		col = AllColors[i%len(AllColors)]

		## Now check if the song only charted 1 week. If so, plot a point.
		if len(songnums) <= 1:
			ax11.scatter(songnums,songranks,color=col)
		else:
			## If the song charted 1 week then fell off until later, plot a plot there.
			if songnums[1]-songnums[0] > 10: ax11.scatter(songnums[0],songranks[0],color=col)
			## Now for each consecutive chartings, if they are consecutive weeks plot
			## a solid line. If they are non-consecutive weeks, plot a faded + dotted line.
			for j in xrange(len(songnums)-1):
				## Calculate the difference between consecutive chartings.
				diff = songnums[j+1]-songnums[j]
				## If more than 7 days, ghost the line.
				if diff > 10: alfa, lss = 0.3, ':'
				else: alfa, lss = 1, '-'
				## Plot.
				ax11.plot(songnums[j:j+2],songranks[j:j+2],color=col,alpha=alfa,ls=lss)
				## If this is an isolated charting that isn't right at the start or end,
				## make a point.
				try: songnums[j-1] - songnums[j+1]
				except IndexError: pass
				if j > 0 and j < len(songnums)-1:
					if songnums[j] - songnums[j-1] > 10 and songnums[j+1] - songnums[j] > 10:
						ax11.scatter(songnums[j],songranks[j],color=col)

		## Plot the song name and save the earliest and latest chart dates for setting the x-axis later.
		ax11.text(songnums[0],spacing[i%13],song.replace("&#039;","'").replace("amp;",""),fontsize=8,color=col)
		FirstDay.append(min(songnums))
		LastDay.append(max(songnums))

	## At this point, if FirstDay and LastDay are empty, then the artist name
	## entered never charted. Inform the user.
	if len(FirstDay) == 0:
		print artist_name, 'does not appear in the Hot 100 records.',
		print 'Please check for typos or if the official band name',
		print 'is different than what you used. For example, "Hall',
		print '& Oates" are actually "Daryl Hall John Oates".'
		quit()

	## Set the bounds of the plot. If specific years were passed, used those.
	## Else, make the plot large enough to encompass all chartings.
	if ForceYears:
		StartYear = str(int(ForceYr1))
		EndYear   = str(int(ForceYr2)+1)
	else:
		StartYear = outdates[min(FirstDay)][:4]
		EndYear   = str(int(outdates[max(LastDay)][:4])+1)

	fig1.set_size_inches(3*(int(EndYear)-int(StartYear)), 5)
	Xstart = StartYear+'-01-01'
	Xend   = EndYear+'-01-01'
	
	## Determine the appropriate tickmarks.
	BigTickDates = [str(int(yr))+'-01-01' for yr in arange(int(StartYear),int(EndYear)+0.5)]
	SmallTkNums = []
	for BTD in BigTickDates:
		## Don't plot small ticks past the last Jan 1.
		if BTD == BigTickDates[-1]: break
		for n in ('02','03','04','05','06','07','08','09','10','11','12'):
			td = BTD.replace('-01-','-'+n+'-')
			try: SmallTkNums.append(outdates.index(td))
			except ValueError: break

	xlocs = [outdates.index(td) for td in BigTickDates]
	xlabs = ['Jan 1 '+td.replace('-01-01','') for td in BigTickDates]

	## Plot lines to indicate #1, 3, 10, and 30
	ax11.plot([0,len(outdates)*1.05],[1,1],'k--',lw=0.5)
	ax11.plot([0,len(outdates)*1.05],[3,3],'k--',lw=0.5,alpha=0.3)
	ax11.plot([0,len(outdates)*1.05],[10,10],'k--',lw=0.5)
	ax11.plot([0,len(outdates)*1.05],[30,30],'k--',lw=0.5,alpha=0.3)

	## Format x axis		
	ax11.set_xlim(outdates.index(Xstart),outdates.index(Xend))
	ax11.xaxis.set_ticks(xlocs)
	ax11.xaxis.set_ticklabels(xlabs)
	ax11.xaxis.set_ticks(SmallTkNums,minor=True)
	ax11.set_xlabel('Date')

	## Format y axis.
	ax11.set_yscale('log')
	ax11.set_ylim(110,0.1)
	ax11.yaxis.set_ticks([100,50,30,20,10,5,3,2,1])
	ax11.yaxis.set_ticklabels(['100','50','30','20','10','5','3','2','1'])
	ax11.set_ylabel('Hot 100 Chart Ranking')

	#pl.subplots_adjust(left=0.03,bottom=0.11,right=0.98,top=0.92)
	pl.title(artist_name+' Hot 100 Rankings')
	pl.tight_layout()

	## Name the plot appropriately
	plot_name = artist_name.replace(' ','')+'_'+str(int(top_x))
	if ForceYears: plot_name += '_'+StartYear+'_'+EndYear
	## Save and show.
	pl.savefig(plot_name+'.png',dpi=250)
	pl.show()


if __name__ == '__main__':

	if   len(sys.argv) == 3:
		## If two args passed, run without forced dates.
		NAME = sys.argv[1]
		TOPX = sys.argv[2]
		artist_plot(NAME,TOPX)
	elif len(sys.argv) == 5:
		## If four args passed, run wit forced dates.
		NAME = sys.argv[1]
		TOPX = sys.argv[2]
		YR1  = sys.argv[3]
		YR2  = sys.argv[4]
		artist_plot(NAME,TOPX,YR1,YR2)
	else:
		## Otherwise, print the instructions.
		print instructions



























