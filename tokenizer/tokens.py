from collections import defaultdict
from bs4 import BeautifulSoup

# Stop Words Set
STOP_WORDS = {  
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren\'t", "as",
    "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can\'t", "cannot",
    "could","couldn\'t", "did", "didn\'t", "do", "does", "doesn\'t", "doing", "don\'t", "down", "during", "each", "few",
    "for", "from", "further", "had", "hadn\'t", "has", "hasn\'t", "have", "haven\'t", "having", "he", "he\'d", "he\'ll",
    "he\'s", "her", "here", "here\'s", "hers", "herself", "him", "himself", "his", "how", "how\'s", "i", "i\'d", "i\'ll",
    "i\'m", "i\'ve", "if", "in", "into", "is", "isn\'t", "it", "it\'s", "its", "itself", "let\'s", "me", "more", "most",
    "mustn\'t", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "also", "this", "will"
}

def tokenize(text):
    """
    Purpose: Takes a string of text as an argument and returns a list of token strings, excluding stop words.
    
    :param text: The text being read character by character.
    :return: The list of all tokens within the text, excluding stop words.
    """
    token_list = []
    current_word = ""
    for char in text:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z' or '0' <= char <= '9':
            char = char.lower()
            current_word += char
        elif current_word:
            # Check if the word is not in stop words
            if current_word not in STOP_WORDS and len(current_word) > 3:
                token_list.append(current_word)
            current_word = ""
    
    # Check the last word if there is any
    if current_word and current_word not in STOP_WORDS:
        token_list.append(current_word)
    
    return token_list

def computeWordFreq(token_list):
    """
    Purpose: Takes a list of tokens as an argument and returns a frequency dictionary.

    :param token_list: The list of tokens
    :return: A default dictionary where 'key' is the token and 'value' is the occurrences
    """
    frequencies = defaultdict(int)
    for word in token_list:
        frequencies[word] += 1
    return frequencies