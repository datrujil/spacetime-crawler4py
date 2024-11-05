import re

STOP_WORDS = {  
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
    "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot",
    "could","couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few",
    "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll",
    "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most",
    "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "also", "this", "will", "the"
}

url_pattern = re.compile(r'URL\d+:\s*(http[s]?://[^\s]+)')

def hashFunction(nGramList):
    hashedGrams = []
    for nGram in nGramList:
        hashValue = sum(int(hash(each) / 2) for each in nGram)
        hashedGrams.append(hashValue)
    return hashedGrams

def fingerprint(file_list, output_file_path):
    with open(output_file_path, "a", encoding="utf-8") as output_file:
        for filename in file_list:
            with open(filename, 'r') as file:
                currUrl = ""
                threeGram = []
                for line in file:
                    # Check if the line contains 'URL#:' and extract the URL if found
                    match = re.search(url_pattern, line)
                    if match:
                        # If a new URL is found and `currUrl` isn't empty, write the previous URL's data to the file
                        if currUrl and threeGram:
                            writeFingerprint(currUrl, threeGram, output_file)
                            threeGram = []  # Reset threeGram list for the new URL
                        currUrl = match.group(1)
                        continue
                    
                    # Tokenize line into alphanumeric tokens, filter stop words and length < 3
                    lineTokens = [token for token in re.findall(r'\b[a-zA-Z0-9]+\b', line.lower())
                                  if token not in STOP_WORDS and len(token) > 2]
                    
                    # Generate 3-grams from the tokens and add to threeGram list
                    threeGram.extend([lineTokens[i:i+3] for i in range(len(lineTokens) - 2)])
                
                # Write the last URL's data if exists after reading the file
                if currUrl and threeGram:
                    writeFingerprint(currUrl, threeGram, output_file)

def writeFingerprint(url, threeGram, output_file):
    hashedGrams = hashFunction(threeGram)
    filtered_hashes = [h for h in hashedGrams if h % 4 == 0]
    output_file.write(f"{url}\n{filtered_hashes}\n\n")

# Example: fingerprint(['./crawled_logs/crawled_content_1.txt'], 'fingerprint_content.txt')