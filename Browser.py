from playwright.sync_api import sync_playwright
import time
import requests
import json
class ChromiumBrowser:
    def __init__(self, proxy=None,reset=0,fake=0):
        self.browser = None
        self.context = None
        self.page = None
        self.proxy = proxy
        self.reset = reset
        self.fake= fake
        self.playwright = sync_playwright().start()
        self.init_browser()

    def init_browser(self):
        browser_args = [
            '--disable-software-rasterizer',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-sync',
            '--disable-translate',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--single-process',
            '--no-sandbox',
            '--disable-application-cache',
            '--disable-offline-load-stale-cache',
            '--disk-cache-size=0',
            '--media-cache-size=0',
            '--no-zygote',
            '--start-maximized',
            '--blink-settings=imagesEnabled=false',
            '--no-first-run',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-background-timer-throttling',
            '--enable-fast-unload',
            '--disable-blink-features=AutomationControlled'
        ]
        
        # Thêm cấu hình proxy nếu biến 'self.proxy' không None
        launch_options = {
            'headless': False,
            'args': browser_args
        }
        if self.proxy:
            if self.reset==1:
                self.change_ip_proxy()
            status=self.check_status_proxy()
            if status == True:
                print(f"Proxy {self.proxy} is ready")
                launch_options['proxy'] = {'server': f'http://{self.proxy}'}
            else:
                pass

        self.browser = self.playwright.chromium.launch(**launch_options)
        self.context = self.browser.new_context(no_viewport=True)
        if self.fake==1:
            cookies = [
            {'name': 'xfa_csrf', 'value': 'tb0lfrvsL0v07iWE', 'domain': 'www.otofun.net', 'path': '/'},
            {'name': 'xfa_user', 'value': '855566%2CPH0D6nJlHaS3EGZkehIVJJrY_61VhyGrplvRhA60', 'domain': 'www.otofun.net', 'path': '/','expiration':8841849156.843996},
            {'name': 'xfa_session', 'value': 'w06avQ34jxbd_m9Lua4l3Pn62uatTDkX', 'domain': 'www.otofun.net', 'path': '/'}
            ]
            self.context.add_cookies(cookies)
            self.page = self.context.new_page()
        else:
            self.page = self.context.new_page()
        # if self.fake==1:
        #     if len(pages) > 1:
        #         pages[0].close()
    def change_ip_proxy(self):
        print(f"Change IP Public of Proxy: {self.proxy}")
        port=str(self.proxy).split(':')[-1]
        url = f'http://192.168.143.101:6868/reset?proxy={port}'
        response = requests.post(url)
        time.sleep(20)
    def check_status_proxy(self):
        print(f"Check status proxy {self.proxy}")
        url=f'http://192.168.143.101:6868/status?proxy={self.proxy}'
        response = requests.post(url)
        json_res=json.loads(response.text)
        if json_res['status'] is True:
            return True
        else:
            return False  
    def close(self):
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()  