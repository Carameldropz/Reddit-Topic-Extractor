import praw
import utility
import re, sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/config")
import import_config
class reddit:
    raw_comments = []
    subreddit = None

    valid_subreddits = ['programming', 'python', 'pokemon', 'minecraft', 
                        'android']

    subreddit_common_words = None

    def __init__(self):
        # Initialize Praw
        r = praw.Reddit(user_agent= \
                        'Topic extraction by /u/topic_extraction_bot')

        not_found = True
        print "Welcome to the reddit topic extractor, a program powered by " + \
              "Python and NLTK that aims to extract current popular topics " + \
              "in a specified subreddit. Please note that larger " + \
              "subreddits have more data to parse and will take longer " + \
              "to process."

        print "Please enter digit representing valid subreddit"
        for i, subreddit in enumerate(self.valid_subreddits):
            print "\t(" + str(i) + ") " + subreddit
        print "\t(Q) to Quit"

        # While the user has not entered a valid name
        while not_found:
            subreddit_name = raw_input()
            if subreddit_name.lower() == "q":
                not_found = False
            else:
                my_num = utility.to_number(subreddit_name)
                if not my_num is None and 0 <= my_num < (len(self.valid_subreddits)):
                    selected_subreddit = self.valid_subreddits[my_num]
                    self.subreddit = r.get_subreddit(selected_subreddit)
                    not_found = False
                    #m_config = __import__("config/" + selected_subreddit + "_config")
                    self.subreddit_common_words = \
                        import_config.get_common_words(selected_subreddit)
                    print "Analyzing " + self.valid_subreddits[my_num]
                else:
                    print "Invalid entry, please enter number in range of 0-" + \
                        str(len(self.valid_subreddits) - 1)

    def is_valid(self):
        """ Check if the current subreddit is valid. 
            @return valid - T/F the subreddit is valid """

        valid = False
        if not self.subreddit == None:
            valid = True
        return valid

    def get_submissions(self, no_submissions):
        """ Grab the specified number of submissions from the current subreddit
            @param no_submissions - Number of submissions to grabs
            @return submissions """

        submissions = self.subreddit.get_hot(limit=no_submissions)
        return submissions

    # Sets the current subreddit
    def set_subreddit(self, name):
        self.subreddit = r.get_subreddit(name)

    def get_flat_comments(self, submission):
        """ Grab all comments from a given submission after converting to ASCII
            @param submission - Submission to extract comments from
            @return raw_comments """

        retry_count = 0
        # Replace all MoreComments objects with their respective comments
        while retry_count < 5:
            try:
                submission.replace_more_comments(limit=None, threshold=0)
                break
            except HTTPError, e:
                retry_count = retry_count + 1
                print "HTTPError while getting all comments - Retrying..."

        # Flatten the comment tree into a list
        my_comments = praw.helpers.flatten_tree(submission.comments)

        # Clear the raw comment list
        del self.raw_comments[:]

        # For each comment, if it isn't null, encode to ASCII and append
        # to the raw comments
        for comment in my_comments:
            if not comment is None:
                if comment.body:
                    string_comment = self.encode_content(comment.body)
                    self.raw_comments.append(string_comment)
        return self.raw_comments

    def encode_content(self, my_content):
        """ Encode the passed content to ASCII
            @param my_content - content to encode
            @return encoded_content """

        return my_content.encode('ascii', 'ignore')
