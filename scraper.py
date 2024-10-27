import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime, timedelta

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # Initialize empty list
    newURLs = []

    # First, check if the status code is 200 so we know we can crawl it
    if (resp.status == 200):
        # Use BeautifulSoups HTML parser
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        # Finds all links within the HTML, searching for all 'a' tags which are the hyperlink tags
        for link in soup.find_all('a'):
            # Since soup returns a tuple, 'href' helps to just grab the URL itself
            url = link.get('href')
            # Check if the url is valid with our given schema
            if (is_valid(url)):
                # If it is, add it to the list of URLs
                # TODO: THIS WILL MESS UP, FIX ISVALID
                newURLs.append(url)

    return newURLs

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    # AF - only add valid links to frontier as per assignment details
    valid_netlocs = ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu', 'today.uci.edu/department/information_computer_sciences']
    # AF - other "invalid" queries
    sharing = 'share='
    actions = 'action='
    calendar_one = 'ical=1'
    calendar_two = 'outlook-ical=1'
    calendar_three = 'post_type=tribe_events'
    calendar_four = 'tribe-bar-date='
    invalid_queries = [sharing, actions, calendar_one, calendar_two, calendar_three, calendar_four]

    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        # AF - only add valid links to frontier as per assignment details
        link_to_be_examined = parsed.netloc
        valid = False
        for valid_link in valid_netlocs:
            if valid_link in link_to_be_examined:
                valid = True
                break
        if not valid:
            return False

         # AF - invalid if contains invalid queries (empirically determined)
        link_to_be_examined = parsed.query
        for other in invalid_queries:
            if other in link_to_be_examined:
                return False

        # AF - url contains a fragment
        link_to_be_examined = parsed.fragment
        if bool(link_to_be_examined):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
