import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

url_order = 0
current_max = [0, ""]

def scraper(url, resp, file):
    """
    Purpose: Main scraping function that validates the response, processes HTML content, and returns valid links.
    Params:
        url: The URL of the web page being scraped.
        resp: The response object from the server, containing the status and raw HTML.
        file: File or logging object used for output or debugging purposes.
    Returns:
        links: A list of valid URLs extracted from the page.
    """
    
    # Check if the response is successful and contains HTML content
    if resp.status == 200:
        # Extract valid links from the page
        links = [link for link in extract_next_links(url, resp, file) if is_valid(link)]

        # Return both the list of valid links and the frequency dictionary
        return links
    
    # If the response is not valid, return empty links and frequencies
    return []

def extract_next_links(url, resp, file):
    """
    Purpose: Extracts all hyperlinks from a web page's HTML content.
    Params:
        url: The base URL of the current web page.
        resp: An object containing the response data, including the raw HTML content.
        file: File or logging object used for output or debugging purposes.
    Returns: A list of URLs found on the page.
    """

    global url_order, current_max
    new_urls = []
    word_minimum = 200  # Minimum word count to consider page as 'high information'


    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

    # Check for low information or undesired content types
    try:
        content_type = resp.raw_response.headers.get('Content-Type', '').lower()
        if content_type == "application/pdf" or content_type == "image/jpeg":
            return new_urls
    except:
        pass

    # Split webpage text content into words and check word count
    webpage_text = soup.get_text().split()
    if len(webpage_text) > word_minimum:
        # Log the page's URL and text content
        url_order += 1
        file.write(f"URL{url_order}: {url}\n{' '.join(webpage_text)}\n\n")

    # Update global max word count if this page has more text
    if len(webpage_text) > current_max[0]:
        current_max = (len(webpage_text), url)

    # Extract valid URLs from anchor tags
    for link in soup.find_all('a', href=True):
        link_url = link.get('href')
        if is_valid(link_url):
            new_urls.append(link_url)
    
    return new_urls

def is_valid(url):
    """
    Purpose: Determines if a given URL should be crawled, returning True for valid URLs and False for invalid ones, based on specific domain constraints and patterns.
    Params:
        url: The URL to be evaluated for validity.
        Returns: True if the URL meets specified criteria for crawling; otherwise, False.
    Notes:
        Utilizes a blacklist of valid domains specific to UCI-related sites.
        Filters out URLs that lead to certain non-content pages, such as calendars.
    """
    
    # only add valid links to frontier as per assignment details
    valid_netlocs = ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu', 'today.uci.edu/department/information_computer_sciences']

    
    # blacklist
    wics_events = "/wics.ics.uci.edu/events"
    undergrad = "/ics.uci.edu/events/category/undergraduate-programs"
    cecs = "https://www.cecs.uci.edu/events"
    cecs_list = "https://www.cecs.uci.edu/events"
    ics_events = "/ics.uci.edu/events"
    ics_cat = "/ics.uci.edu/events"
    isg = "/isg.ics.uci.edu/events"
    physics = "physics.uci.edu"
    cecs = "cecs.uci.edu"
    eecs = "eecs.uci.edu"
    nacs = "nacs.uci.edu"
    linguistics = "linguistics.uci.edu"
    statistics = "statistics.uci.edu"
    economics = "economics.uci.edu"

    # other problematic
    pdf = "/pdf"
    ppsx = ".ppsx"
    odc = ".odc"
    nb = ".nb"
    py = ".py"
    webp = ".webp"

    blacklist = [wics_events, undergrad, cecs, cecs_list, ics_events, ics_cat, isg, pdf, ppsx, odc, nb, py, webp, physics, cecs, eecs, nacs, linguistics, statistics, economics]

    # errors in the domain
    your_ip_one = "[YOUR_IP]"
    your_ip_two = "YOUR_IP"
    public_ip = "PUBLIC_IP"
    local_host = "localhost"
    aws_public_id = "[YOUR-AWS-PUBLIC-IP]"
    invalid_domains = [your_ip_one, your_ip_two, public_ip, local_host, aws_public_id]

    # other "invalid" queries
    sharing = 'share='
    actions = 'action='
    calendar_one = 'ical=1'
    calendar_two = 'outlook-ical=1'
    calendar_three = 'post_type=tribe_events'
    calendar_four = 'tribe-bar-date='
    filtering = "filter"
    invalid_queries = [sharing, actions, calendar_one, calendar_two, calendar_three, calendar_four, filtering]

    try:
        
        # extraneous error, check first
        if url is None:
            return False

        # check for errors in the domain
        for domain_error in invalid_domains:
            if domain_error in url:
                return False

        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        # check blacklist (avoiding bad urls)
        for blacklisted_url in blacklist:
            if blacklisted_url in url:
                return False

        # only add valid links to frontier as per assignment details
        link_to_be_examined = parsed.netloc
        valid = False
        for valid_link in valid_netlocs:
            if valid_link in link_to_be_examined:
                valid = True
                break
        if not valid:
            return False
    
        # invalid if contains invalid queries
        link_to_be_examined = parsed.query
        for other in invalid_queries:
            if other in link_to_be_examined:
                return False

        # url contains a fragment
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
