import re
from collections import Counter

STOP_WORDS = {  
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
    "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot",
    "could","couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few",
    "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll",
    "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most",
    "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", 
    "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when",
    "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

def top_50_tokens(file_list):
    token_counts = Counter()  # Initialize a single Counter to store counts across all files
    
    for filename in file_list:
        with open(filename, 'r') as file:
            for line in file:
                # Filter out HTTP links
                if 'http' in line:
                    continue
                
                # Tokenize using regex to find alphanumeric words only
                for token in re.findall(r'\b[a-zA-Z0-9]+\b', line.lower()):
                    # Exclude stop words and words less than 2 letters
                    if token not in STOP_WORDS and len(token) > 2:
                        token_counts[token] += 1

    # Get the top 50 most common tokens across all files: most_common() is a Counter() method
    top_50 = token_counts.most_common(50)

    # Print the top 50 tokens
    for token, count in top_50:
        print(f"{token} -> {count}")

# Example Usage
# top_50_tokens(['./crawled_logs/crawled_content_1.txt', './crawled_logs/crawled_content_2.txt', './crawled_logs/crawled_content_3.txt', './crawled_logs/crawled_content_4.txt', './crawled_logs/crawled_content_5.txt', './crawled_logs/crawled_content_6.txt', './crawled_logs/crawled_content_7.txt', './crawled_logs/crawled_content_8.txt', './crawled_logs/crawled_content_9.txt', './crawled_logs/crawled_content_10.txt', './crawled_logs/crawled_content_11.txt', './crawled_logs/crawled_content_12.txt', './crawled_logs/crawled_content_13.txt', './crawled_logs/crawled_content_14.txt'])