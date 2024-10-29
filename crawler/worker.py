from threading import Thread
from inspect import getsource
from utils.download import download


from utils import get_logger
import scraper
import time

class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier

        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        file_count = 1
        urls_processed = 0
    
        output_file_path = f"crawled_content_{file_count}.txt"
        file = open(output_file_path, "a", encoding="utf-8")
    
        try:
            #counter = 0
            while True:

                tbd_url = self.frontier.get_tbd_url()
                if not tbd_url:
                    self.logger.info("Frontier is empty. Stopping Crawler.")
                    break
    
                resp = download(tbd_url, self.config, self.logger)
                self.logger.info(
                    f"Downloaded {tbd_url}, status <{resp.status}>, "
                    f"using cache {self.config.cache_server}.")
    
                # DT - Get scraped URLs and token frequencies
                scraped_urls = scraper.scraper(tbd_url, resp, file)

                urls_processed += 1

                if urls_processed >= 1000:
                    file.close()
                    file_count += 1
                    urls_processed = 0
                    output_file_path = f"crawled_content_{file_count}.txt"
                    file = open(output_file_path, "a", encoding="utf-8")

                for scraped_url in scraped_urls:
                    self.frontier.add_url(scraped_url)
                self.frontier.mark_url_complete(tbd_url)
                time.sleep(self.config.time_delay)
                #counter = counter + 1
        finally:

            file.close()
            results_file = f"crawled_analysis.txt"
            file = open(results_file, "a", encoding="utf-8")
            file.write(f"Insert Domain Dict\nMax words : URL -> {scraper.current_max}\nInsert Unique URL Count\n")
            file.close()
