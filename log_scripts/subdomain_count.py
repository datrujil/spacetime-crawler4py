import re
from urllib.parse import urlparse
from collections import defaultdict

def extract_subdomains(file_paths):
    subdomain_count = defaultdict(set)  # Stores subdomains

    # Regular expression to match: "URL" followed by numbers and a URL
    url_pattern = re.compile(r'^URL\d+:\s*(https?://\S+)')
    
    # Iterate over each file path provided
    for file_path in file_paths:
        # Open and read the file line by line
        with open(file_path, 'r') as file:
            for line in file:
                match = url_pattern.match(line)
                if match:
                    url = match.group(1)
                    parsed_url = urlparse(url) # Parses URL into a url and it's scheme
                    
                    # Check if the domain is uci.edu
                    if parsed_url.hostname.endswith('.uci.edu'):
                        # Split URL by the period
                        # Ex: www.ics.uci.edu --> ['www', 'ics', 'uci', 'edu']
                        domain_parts = parsed_url.hostname.split('.')
                        
                        # If there are at least 3 parts, we can identify subdomains
                        # If there's less, then we are just in the domain (i.e. "uci.edu")
                        if len(domain_parts) > 2:
                            # Remove "www" if it's present and join the remaining parts
                            subdomain = '.'.join(part for part in domain_parts[:-2] if part != 'www')
                            
                            # Ensure we only keep unique URLs for counting
                            subdomain_count[subdomain].add(url)  # Add the full URL to the set for uniqueness

    return subdomain_count

def format_output(subdomain_count):
    # Sort subdomains alphabetically and format the output
    sorted_subdomains = sorted(subdomain_count.items())
    output = []
    for subdomain, pages in sorted_subdomains:
        output.append(f"{subdomain}, {len(pages)}")  # Format as "subdomain, count"
    return output

# Example of how to use it
# file_paths = ['crawler_log_1.txt', 'crawler_log_2.txt']
# extracted_subdomains = extract_subdomains(file_paths)
# formatted_output = format_output(extracted_subdomains)

# Output the results
for line in formatted_output:
    print(line)