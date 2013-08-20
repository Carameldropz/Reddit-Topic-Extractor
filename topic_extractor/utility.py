import re
import nltk

# Regex modified from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
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

def remove_urls(my_text):
    """ Given a provided text, removes all urls.
        @param my_text - text to evaluate for urls
        @return new_text - text with urls removed """

    new_text = re.sub(url_grammar, "", my_text)
    return new_text

def ExtractPhrases(myTree, phrase):
    """ Taken from monlp link at top.
        Extracts the given phrase types from the passed tree.
        @param myTree - tree to evaluate for phrases
        @param phrase - phrase to search for 
        @return myPhrases - list of phrases extracted """

    myPhrases = []
    if (myTree.node == phrase):
        myPhrases.append(myTree.copy(True))
    for child in myTree:
        if (type(child) is nltk.tree.Tree):
            list_of_phrases = ExtractPhrases(child, phrase)
            if (len(list_of_phrases) > 0):
                myPhrases.extend(list_of_phrases)
    return myPhrases

def remove_tree_formatting(entry):
    """ Extract the tree formatting.
        Remove:
             - (, )
             - /NNP, /NNS, /NN
             - NP
             - /JJS, /JJ
             - /PRP
        @param entry - Tree entry to remove formatting from
        @return entry - Cleaned entry """

    if (type(entry) is str):
        entry = entry.replace("(", "")
        entry = entry.replace(")", "")
        entry = entry.replace("/NNP", "")
        entry = entry.replace("/NNS", "")
        entry = entry.replace("NP ", "")
        entry = entry.replace("/NN", "")
        entry = entry.replace("/JJS", "")
        entry = entry.replace("/JJ", "")
        entry = entry.replace("/PRP$", "")
        entry = entry.replace("/IN", "")
        entry = entry.replace("NADJ ", "")

    return entry

def to_number(m_string):
    try:
        m_num = int(m_string)
        return m_num
    except ValueError:
        return None
