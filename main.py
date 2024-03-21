import threading
from crawler import OtoFunCrawler

if __name__ == "__main__":
    crawler = OtoFunCrawler()
    url='https://www.otofun.net/whats-new/posts'
    thread1 = threading.Thread(target=crawler.get_link,args=(url,))
    thread2 = threading.Thread(target=crawler.get_all)

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()