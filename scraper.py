import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime, timedelta
from tokenizer.tokens import tokenize, computeWordFreq
from collections import defaultdict

url_order = 0
current_max = [0, ""]

def processHTMLContent(html_content):
    """ DT - 
    Processes HTML content, extracts text, tokenizes, and returns a frequency dictionary.
    :param html_content: HTML string to be processed.
    :return: A dictionary with token frequencies for the HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    
    tokens = tokenize(text_content)
    return computeWordFreq(tokens)
    current_max = (0, "")

def scraper(url, resp, file):
    # DT - Check if the response is successful and contains HTML content
    if resp.status == 200:
        # DT - Extract valid links from the page
        links = [link for link in extract_next_links(url, resp, file) if is_valid(link)]
        
        # DT - Process the HTML content and get token frequencies
        frequencies = processHTMLContent(resp.raw_response.content)
        
        # DT - Return both the list of valid links and the frequency dictionary
        return links, frequencies
    
    # DT - If the response is not valid, return empty links and frequencies
    return [], defaultdict(int)

def extract_next_links(url, resp, file):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the urlnot  again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    global url_order
    
    # Initialize empty list
    newURLs = []

    # First, check if the status code is 200 so we know we can crawl it
    if (resp.status == 200):
        # Use BeautifulSoups HTML parser
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        # AF - determine if webpage is 'low information'
        word_minimum = 200
        webpage_text = soup.get_text().split()
        is_pdf = False

        try:

            if resp.raw_response.headers.get('Content-Type') == "application/pdf":
                is_pdf = True
        except:
            pass
        if not is_pdf:
            if len(webpage_text) < word_minimum:
                pass
            elif resp.raw_response.headers.get('Content-Type') == "image/jpeg":
                pass
            else:
                global current_max
                
                if len(webpage_text) > current_max[0]:
                    current_max[0] = len(webpage_text)
                    current_max[1] = url 

                url_order += 1
                
                file.write(f"URL{url_order}: {url}\n{webpage_text}\n\n")
                
                # Finds all links within the HTML, searching for all 'a' tags which are the hyperlink tags
                for link in soup.find_all('a'):
                    
                    # Since soup returns a tuple, 'href' helps to just grab the URL itself
                    url = link.get('href')
                    # Check if the url is valid with our given schema
                    if (is_valid(url)):
                        
                        # If it is, add it to the list of URLs
                        newURLs.append(url)
    
                        parsed_url = urlparse(url)
    return newURLs

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    # AF - only add valid links to frontier as per assignment details
    valid_netlocs = ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu', 'today.uci.edu/department/information_computer_sciences']

    # AF - whitelist (avoid these urls since they lead to calendars)
    # AF - whitelist (avoid these urls since they lead to calendars)
    wics_cat = "https://wics.ics.uci.edu/events/category/"
    wics = "/wics"
    undergrad = "https://ics.uci.edu/events/category/undergraduate-programs"
    other = "https://ngs.ics.uci.edu"
    pdf = "/pdf"
    ppsx = ".ppsx"
    odc = ".odc"

    # DT - more trap hyperlinks
    wics_events = "https://wics.ics.uci.edu/events/"
    cecs = "https://www.cecs.uci.edu/events/"
    cecs_list = "https://www.cecs.uci.edu/events/list"
    ics_events = "https://ics.uci.edu/events/"
    ics_cat = "https://ics.uci.edu/events/category/"
    isg = "https://isg.ics.uci.edu/events/"
    py = ".py"

    whitelist = [ppsx, odc, wics, wics_cat, wics_events, undergrad, cecs, cecs_list, ics_events, ics_cat, isg, other, py, pdf]



    # AF - errors in the domain
    your_ip_one = "[YOUR_IP]"
    your_ip_two = "YOUR_IP"
    public_ip = "PUBLIC_IP"
    local_host = "localhost"
    aws_public_id = "[YOUR-AWS-PUBLIC-IP]"
    invalid_domains = [your_ip_one, your_ip_two, public_ip, local_host, aws_public_id]

    # AF - other "invalid" queries
    sharing = 'share='
    actions = 'action='
    calendar_one = 'ical=1'
    calendar_two = 'outlook-ical=1'
    calendar_three = 'post_type=tribe_events'
    calendar_four = 'tribe-bar-date='
    filtering = "filter"
    invalid_queries = [sharing, actions, calendar_one, calendar_two, calendar_three, calendar_four, filtering]

    try:
        
        # AF - extraneous error, check first
        if url is None:
            return False

        # AF - check for errors in the domain
        for domain_error in invalid_domains:
            if domain_error in url:
                return False

        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        # AF - check whitelist (avoiding urls that lead to calendars)
        for whitelisted_url in whitelist:
            if whitelisted_url in url:
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
