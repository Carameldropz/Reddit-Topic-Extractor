# @author Evelina Arthursson
# 
# Outside sources used:
# www.monlp.com/2012/01/20/extracting-noun-phrases-from-parsed-trees/
# http://daringfireball.net/2010/07/improved_regex_for_matching_urls
#

import nltk
import common_words, reddit_interface, utility
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

class reddit_analyzer:

    my_reddit = None

    # Grammar for noun phrases
    m_grammar = r"""
        NADJ: {<JJ.*>*<NN.*>+}
        NP: 
            {<PRP$>?<NADJ>}
            {<NADJ><IN><NADJ>}
        """

    # Regex modified from 
    # http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    url_grammar = r"""
                (?xi)
                \b
                ( # Capture 1: entire matched URL
                  (?:
                    https?://                   # http or https protocol
                    |                           #   or
                    www\d{0,3}[.]               # "www.", "www1.", "www2." "www999."
                    |                           #   or
                    [a-z0-9.\-]+[.][a-z]{2,4}/  # looks like domain name followed by a slash
                  )
                  (?:                           # One or more:
                    [^\s()<>\[\]]+              # Run of non-space, non-()<>
                    |                           #   or
                    \(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\)  # balanced parens, up to 2 levels
                  )+
                  (?:                           # End with:
                    \(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\)  # balanced parens, up to 2 levels
                    |                           #   or
                    [^\s`!()\[\]{};:'".,<>?]    # not a space or one of these punct chars
                  )
                )
            """

    cp = nltk.RegexpParser(m_grammar)

    # Symbols we want to disregard
    irrelevant_symbols = ["!", "(", ")", "[", "]", "", " ",
                            "{", "}", "/", "\\", "^", "%", "/sp",
                            "=", "-", "_"]

    def __init__(self):
        self.my_reddit = reddit_interface.reddit()

    def subreddit_valid(self):
        return self.my_reddit.is_valid()

    def analyze_content(self, no_submissions):
        """ Processes the specified number of submissions.
            Fetches submissions and analyzes those submissions one by one and
            then incrementing our master submission freq dist to keep track
            of how often topics are being mentioned.

            After analysis is complete, up to 50 of the topic topics are 
            printed or until submissions with more than 3 mentions run out.
            @param no_submissions - The number of submissions to pull """

        print "Fetching submissions... ",
        m_submissions = self.my_reddit.get_submissions(no_submissions)
            
        print "Done"

        submission_fDist = nltk.FreqDist()

        print "Starting Submission Processing... "
        for submission in m_submissions:
            print '.',
            # Get a frequency dist for the topics in this submission
            my_fDist = self.analyze_submission(submission)
            # For each entry in the freq dist increment our master freq dist
            for sample in my_fDist:
                for i in range(my_fDist[sample]):
                    submission_fDist.inc(sample)
        print "Done"

        count = 0
        for sample in submission_fDist:
            if count > 50:
                break
            # If the current sample was mentioned more than once
            if submission_fDist[sample] > 3:
                print "(" + sample + ", " + \
                            str(submission_fDist[sample]) + ") ",
            count = count + 1

    def extract_noun_phrases(self, text):
        """ Tokenizing the text into sentences, and then those sentences get 
            tokenized into indifidual words. Tokenized sentences are then 
            pos tagged and parsed for noun phrases. These noun phrases are 
            then cleared of their tree formatting and added to our noun phrase
            list.
            @param text - Text to extract noun phrases from
            @return complete_list - list of extracted noun phrases """

        # Tokenize text into sentences
        n_text_sents = nltk.sent_tokenize(text)
        complete_list = []

        # For each sentence
        for sent in n_text_sents:
            # Tokenize and pos tag words in sentence
            n_text = nltk.word_tokenize(sent)
            pos_tagged = nltk.pos_tag(n_text)

            # Parse the resulting tree and extract the noun phrases
            parse_tree = self.cp.parse(pos_tagged)
            list_of_phrases = utility.ExtractPhrases(parse_tree, "NP")

            # For each phrase of the noun phrases extracted
            for phrase in list_of_phrases:
                # Remove the formatting and append to list to be returned
                removed_tree_formatting = \
                    utility.remove_tree_formatting(nltk.tree.Tree.pprint(phrase))
                complete_list.append(removed_tree_formatting)

        return complete_list

    def compileTopics(self, list_of_lists):
        """ Take the list of lists and create a frequency distribution by 
            taking each individual item and counting how many times it 
            appears within the list of lists.
            @param list_of_lists - List of noun phrase lists
            @return freqDist - frequency distribution of all compiled topics """

        freqDist = nltk.FreqDist()
        for l in list_of_lists:
            for item in l:
                # Check if item is a symbol or common word
                if not item in self.irrelevant_symbols and not \
                                item in common_words.common_words and not \
                                item in self.my_reddit.subreddit_common_words:
                    freqDist.inc(item)
        return freqDist

    def analyze_comment(self, comment):
        """ Analyze a single comment after lowercasing and removing all urls.
            Comments are parsed to extract noun phrases.
            @param comment - The comment to parse
            @return noun_phrases - All noun phrases gathered from a single 
            comment """

        noun_phrases = []

        # Remove urls from raw comment
        n_comment = utility.remove_urls(comment.lower())
        if n_comment.replace(" ", ""):
            noun_phrases = self.extract_noun_phrases(n_comment)
        return noun_phrases

    def analyze_submission(self, submission):
        """ Analyze a single submission first on a comment level and then 
            compiling all noun phrases found in a frequency distribution.
            @param submission - The submission to analyze
            @return my_fDist - A freq distribution of all compiled topics for
            a submission. """

        comment_list = []
        print ".",

        # Grab all comments from a submission
        for comment in self.my_reddit.get_flat_comments(submission):
            # Get all noun phrases from a single comment
            noun_phrases = self.analyze_comment(comment)
            # If list not empty
            if noun_phrases:
                comment_list.append(noun_phrases)

        # Compile all topics from the comment list
        my_fDist = self.compileTopics(comment_list)
        return my_fDist
