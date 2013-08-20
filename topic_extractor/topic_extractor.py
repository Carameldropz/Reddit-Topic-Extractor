import analyzer

my_analyzer = analyzer.reddit_analyzer()

# Check to make sure we have a valid subreddit object
if my_analyzer.subreddit_valid():
    my_analyzer.analyze_content(30)
