# hot100plots

Hot100Plot.py

This program produces a plot of the chart locations of every song by 
a specified artist on the Billboard Hot 100 chart since it's inception
in 1958. This program can be called in one of two ways.

1) Pass two arguments.
	artist_name (str) = The name of the band/artist. If the name contains a space, put it in quotes.
	top_x       (int) = Only consider chartings within the top X. I.E. top 100, top 50, top 10, etc.

	example: python Hot100Plot.py "Taylor Swift" 100

2) Pass four arguments.
	artist_name (str) = Same as above.
	top_x       (int) = Same as above.
	ForceYr1    (int) = Force the chart to begin on Jan 1 of a specified year.
	ForceYr2    (int) = Force the chart to end on Dec 31 of a specified year.

	example: python Hot100Plot.py Madonna 50 1983 2004

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
  
  
  
  GetNewChart.py
  
This program uses wget to query the Billboard Hot 100 website for a specific date. It then parses the resulting .html file into a more easily usable format.

This program can only be called one way, by passing one argument -- the date in the format YYYY-MM-DD.

  For example: python GetNewChart.py 2018-07-28

If wget and parsing are successful, it will ask if you want to delete the html original, which you can do by responding "y" at the prompt. The resulting file will have the name of the passed date, and should be 100 lines long, which each line containing a chart ranking, song title, and artist title separated by commas.

Billboard published a new Hot 100 chart every Tuesday, with data from the last Friday-Thursday period. A single date is associated with each chart, corresponding to the Saturday which immediately follows the Tuesday of publishing. Ideally you should query the date of this Saturday as this is the official date for the chart, and plots produced with this chart will thus have the correct publish date. However, querying other days will also download the chart for whichever week that date happens to fall into.



hot100charts

This is the file containing all of the parsed charts. The files are pretty self-explanatory.
