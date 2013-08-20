
def get_common_words(subreddit_name):
    m_config = __import__(subreddit_name + "_config")
    return m_config.common_words
