from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    # Split each string into lines
    a_list = a.splitlines()
    b_list = b.splitlines()
    # Create a set of lines that are in a & b
    sim_lines = {i for i in a_list if i in b_list}
    # Return the set
    return sim_lines


def sentences(a, b):
    """Return sentences in both a and b"""
    # Split each string into sentences with sent_tokenize
    a_list = sent_tokenize(a, language='english')
    b_list = sent_tokenize(b, language='english')
    # Create a set of sentences that are in a & b
    sim_sent = {i for i in a_list if i in b_list}
    # Return the set
    return sim_sent


def stringer(text, n):
    """Return list of substrings with length n for passed in text"""
    # Sets length modified to prevent slices smaller than n
    length = (len(text) - n) + 1
    # Slice string text with n == slice size
    text_list = [text[i:i + n] for i in range(0, length)]
    # Return list of slices
    return text_list


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    # Split each string into substrings with stringer()
    a_list = stringer(a, n)
    b_list = stringer(b, n)
    # Create a set of substrings that are in a & b
    sim_sub = {i for i in a_list if i in b_list}
    # Return the set
    return sim_sub