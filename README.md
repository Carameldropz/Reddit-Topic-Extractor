Reddit-Topic-Extractor
======================

Extracts hot topics from a subreddit of choice and display some of the most popular at the time of running the program.

Required:
----------------------
    * Python (python.org/download)
    * NLTK (nltk.org/install.html)
    * Praw: Reddit API Wrapper (github.com/praw-dev/praw)

Example
----------------------
<pre>python topic_extractor.py
Welcome to the reddit topic extractor, a program powered by Python and NLTK that aims to extract
current popular topics in a specified subreddit. Please note that larger subreddits have more
data to parse and will take longer to process.
Please enter digit representing valid subreddit
	(0) programming
	(1) python
	(2) pokemon
	(3) minecraft
	(4) android
	(Q) to Quit
4
Analyzing android
Fetching submissions...  Done
Starting Submission Processing... 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . Done
(nexus, 98)  (htc, 81)  (waze, 64)  (iphone, 48)  (tv, 44)  (tasker, 42)  (battery, 40)  
(ipad, 40)  (battery life, 39)  (ios, 39)  (n4, 36)  (google, 35)  (cm, 34)  (tablet, 29)
(swype, 26)  (moto x, 25)  (swiftkey, 25)  (youtube, 25)  (motorola, 24)  (chromecast, 23)
(root, 23)  (s4, 23)  (apple, 22)  (keyboard, 22)  (ron, 22)  (flagship, 21)  
(google maps, 21)  (maps, 21)  (maxx, 21)  (developer, 20)  (note, 20)  (poweramp, 20)  
(support, 20)  (ads, 19)  (display, 19)  (roms, 19)  (sale, 19)  (rom, 18)  (sd card, 18)  
(ui, 18)  (wifi, 18)  (amp, 17)  (gnex, 17)  (link, 17)  (mini, 17)  (play store, 17)  
(ppi, 17)  (thread, 17)  (apk, 16)  (camera, 16)  (galaxy nexus, 16) 
</pre>
