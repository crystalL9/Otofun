from datetime import datetime
import json
import time
import queue
import urllib.parse
import pytz
import re
from Browser import ChromiumBrowser
    
class OtoFunCrawler :
    link_queue = queue.Queue()
    reactions_queue = queue.Queue()
    domain='https://www.otofun.net'
    json_file_path = 'dev_config.json'
    with open(json_file_path, 'r') as file:
            data = json.load(file)
    proxy_post=data['proxy_post']
    proxy_link=data['proxy_link']
    fake=data['use_cookie']
    reset=data['use_proxy']
    def get_spec_post(self,page):
        # page=ChromiumBrowser(fake=1).page
        data_crawl={}
        current_time = datetime.now()
        timestamp = current_time.timestamp()
        data_crawl['time_crawl']=int(timestamp)
        type='xamvn post'
        data_crawl['type'] = type
        data_crawl['domain']=self.domain
        article=page.query_selector_all('article')[0]
        data_crawl['author'] = article.get_attribute('data-author')

        div_avatar = article.query_selector('aside.message-articleUserInfo')
        a_element = div_avatar.query_selector('a')
        link_author= a_element.get_attribute('href')
        id_user= a_element.get_attribute('data-user-id')
        data_crawl['id_author'] = id_user
        data_crawl['author_link']=self.domain+link_author
        id=article.get_attribute('id')
        data_crawl['id'] = id
        data_crawl['source_id'] = ''

        title_element=page.query_selector_all('div.p-title')[0]
        data_crawl['title']=title_element.inner_text()
        if 'xa0' in data_crawl['title']:
            data_crawl['title'] =  data_crawl['title'].split('xa0')[-1]

        li_element = article.query_selector('li.u-concealed')
        a_element = li_element.query_selector( 'a')
        href = a_element.get_attribute('href')
        data_crawl['link']=self.domain+href
        time_element = a_element.query_selector('time')
        datetime_value = time_element.get_attribute('data-time')
        data_crawl['created_time']=int(datetime_value)
        
        # data_crawl['comments']=cmt
        # data_crawl['views']=view

        txt=''
        hrefs=[]
        try:
            extra_link_element = article.query_selector_all("a.link.link--external.fauxBlockLink-blockLink")
            hrefs = [element.get_attribute('href') for element in extra_link_element]
        except:
            pass
        data_crawl['out_links']=hrefs

        # for l in outlink:
        #     data_crawl['content']= data_crawl['content'].replace('\n\xa0', '').replace("Click to expand...", "").replace(txt,"").replace(l,"")
        data_crawl['image_url']=[]
        bbwrapper = page.query_selector_all("div.bbWrapper")[0]
        data_crawl['content']= bbwrapper.inner_text()
        images = bbwrapper.query_selector_all("img")

        for img in images:
            src = img.get_attribute('src')
            if src:
                data_crawl['image_url'].append(src)
            else:
                href = img.get_attribute('href')
                if href:
                    data_crawl['image_url'].append(href)
            
        data_crawl['image_url'] = [x for x in data_crawl['image_url'] if x is not None and x != '']
        data_crawl['videos']=[]
        player = page.query_selector_all('span.s9e-miniplayer-inactive')
        if player:
            for p in player:
                video_elements = p.query_selector_all('iframe')
                for v in video_elements:
                    video_link = v.get_attribute('src')
                    data_crawl['videos'].append(video_link)
        videos_tag=page.query_selector_all('video.videotag')
        if videos_tag:
            for vt in videos_tag:
                sources=vt.query_selector_all('source')
                for s in sources:
                    video_link = s.get_attribute('src')
                    data_crawl['videos'].append(video_link)
        data_crawl['videos'] = [x for x in data_crawl['videos'] if x is not None and x != '']
        list_angry=[]
        list_like=[]
        list_haha=[]
        list_wow=[]
        list_love=[]
        try:
            href = article.query_selector('.reactionsBar-link').get_attribute('href')
            xpath_expression = f"//a[@href='{href}']"
            link_to_click = page.query_selector(xpath_expression)
            if link_to_click:
                link_to_click.click()
                time.sleep(1)
                page.wait_for_selector("div.overlay-container.is-active")

                elements = page.query_selector_all('li.block-row.block-row--separated')
                for e in elements:
                    user={}
                    avatar_element = e.query_selector('.avatar.avatar--s')
                    user_id = avatar_element.get_attribute('data-user-id')
                    link_user = self.domain+avatar_element.get_attribute('href')
                    img = avatar_element.query_selector('img')
                    if img:
                            src = img.get_attribute('src')
                            name = img.get_attribute('alt')
                    else:
                        src=''
                        span = avatar_element.query_selector('span')
                        name = span.get_attribute('aria-label')

                    div_element = e.query_selector('div.contentRow-extra')
                    span_element = div_element.query_selector('span')
                    reaction_id = span_element.get_attribute('data-reaction-id')
                    time_element = div_element.query_selector('time')
                    reacted_time = time_element.get_attribute('data-time')

                    div_element_2 = e.query_selector('div.contentRow-lesser')
                    role_element = div_element_2.query_selector('span.userTitle')
                    role = role_element.inner_text()
                    try:
                        loaction_element = div_element_2.query_selector('a')
                        link_location = self.domain+loaction_element.get_attribute('href')
                        location = loaction_element.inner_text() 
                    except:
                        link_location=''
                        location=''
                        pass

                    div_element_3 = e.query_selector('div.contentRow-minor')
                    li_elements = div_element_3.query_selector_all('li')
                    str_number=''
                    for li in li_elements:
                        dl_element= li.query_selector('dl.pairs.pairs--inline')
                        dd_element = dl_element.query_selector('dd')
                        number = dd_element.inner_text()+'|'
                        str_number+=number
                    user['author'] = name
                    user['id_author']= user_id
                    user['role']= role
                    user['author_link']= link_user
                    user['avatar']= self.domain+src
                    user['location']= location
                    user['location_link']=link_location
                    user['messages']=float(str_number.split('|')[0].replace(',','.'))
                    user['reactions_points'] = float(str_number.split('|')[1].replace(',','.'))
                    user['points'] = int(str_number.split('|')[2])
                    user['reacted_time']=int(reacted_time)
                    if reaction_id=='1':
                        list_like.append(user)
                    elif reaction_id=='2':
                        list_love.append(user)
                    elif reaction_id=='3':
                        list_haha.append(user)
                    elif reaction_id=='4':
                        list_wow.append(user)
                    elif reaction_id=='6':
                        list_angry.append(user)
                page.press('body', 'Escape')
        except:
            pass
        data_crawl['angry']=len(list_angry)
        data_crawl['list_angry']=list_angry
        data_crawl['like']= len(list_like)
        data_crawl['list_like']=list_like
        data_crawl['haha']=len(list_haha)
        data_crawl['list_haha']=list_haha
        data_crawl['love']=len(list_love)
        data_crawl['list_love']=list_love
        data_crawl['wow']=len(list_wow)
        data_crawl['list_wow']=list_wow
        self.save_data(data_crawl)

    def get_all(self):
        while True:
            if not self.link_queue.empty():
                try:
                    str_link=self.link_queue.get()
                    url=str_link.split('|')[0]
                    cmt=str_link.split('|')[1]
                    view=str_link.split('|')[2]
                    print(f"Crawl all data of all pages from {url}")
                    chromium=ChromiumBrowser()
                    try:
                        chromium.page.goto(url,timeout=600000)
                    except:
                        chromium.page.reload(timeout=600000)
                        pass
                    div_spec_selector = "div.block.block--messages[data-xf-init='lightbox select-to-quote']"
                    d = chromium.page.query_selector(div_spec_selector)
                    if d:
                        self.get_spec_post(page=chromium.page)
                    page_num = 0
                    article_post = chromium.page.query_selector_all('article')[0]
                    source_id = article_post.get_attribute('id')
                    title_element = chromium.page.query_selector_all('div.p-title')[0]
                    title = title_element.inner_text()
                    if '\xa0' in title:
                        title=title.split('\xa0')[-1]
                    next_link =''
                    while next_link != None:
                        if page_num > 0:
                            try:
                                chromium.page.goto(url,timeout=600000)
                                chromium.page.reload(timeout=600000)
                            except:
                                chromium.page.reload(timeout=600000)
                                pass
                        try:
                            next_link_elm = chromium.page.query_selector('a.pageNav-jump.pageNav-jump--next')
                            next_link = self.domain+next_link_elm.get_attribute('href')
                            url=next_link
                        except:
                            next_link = None
                        count=0
                        articles = chromium.page.query_selector_all('article.message.message--post.js-post.js-inlineModContainer')
                        for article in articles:
                            count+=1
                            print(f"--->>>>>>{count}")
                            try:
                                chromium.page.evaluate('(element) => element.scrollIntoView()', article)
                                time.sleep(0.5)
                                data_crawl={}
                                itemtype = article.get_attribute('itemtype')
                                if itemtype or count>1:
                                    type = 'xamvn comment'
                                else:
                                    type = 'xamvn post'
                                
                                current_time = datetime.now()
                                timestamp = current_time.timestamp()
                                data_crawl['time_crawl']=int(timestamp)
                                data_crawl['type']=type
                                data_crawl['domain']= self.domain
                                data_crawl['author'] = article.get_attribute('data-author')
                                id_post=article.get_attribute('id')
                                div_avatar = article.query_selector('div.message-avatar-wrapper')
                                a_element = div_avatar.query_selector('a')
                                link_author= a_element.get_attribute('href')
                                id_user= a_element.get_attribute('data-user-id')
                                data_crawl['id_author'] = id_user
                                data_crawl['author_link']=self.domain+link_author




                                try:
                                    img_element = a_element.query_selector('img')
                                    src_avatar = img_element.get_attribute('src')
                                except:
                                    src_avatar= None
                                if src_avatar:
                                    data_crawl['avatar']=self.domain+src_avatar
                                else:
                                    data_crawl['avatar']=''
                                user_detail_divs = article.query_selector('div.message-userDetails')
                                user_title_element = user_detail_divs.query_selector('.userTitle.message-userTitle')
                                role = user_title_element.inner_text()
                                data_crawl['role']=role

                                user_extras_div = article.query_selector('div.message-userExtras')
                                list_dl =user_extras_div.query_selector_all('dl')
                                # data_crawl['joined_time'] = list_dl[1].inner_text()
                                # data_crawl['km'] = int(list_dl[2].inner_text().replace(',',''))
                                # data_crawl['engine'] = int(list_dl[3].inner_text().replace(',','').split(' ')[0])

                                if type=='xamvn comment':
                                    data_crawl['source_id']=source_id
                                    data_crawl['title']= ''
                                    data_crawl['comments']= 0
                                    data_crawl['views'] = 0
                                elif type == 'xamvn post':
                                    data_crawl['source_id']=''
                                    data_crawl['title']= title
                                    data_crawl['comments']= cmt
                                    data_crawl['views'] = view

                                # lấy link bài và thời gian đăng bài
                                div_time_element = article.query_selector('div.message-attribution-main')
                                a_element = div_time_element.query_selector( 'a')
                                href = a_element.get_attribute('href')
                                data_crawl['link']=self.domain+href
                                # time_element = a_element.query_selector('time')
                                datetime_value = a_element.inner_text()
                                data_crawl['created_time']=self.txt_to_timestamp(datetime_value)
                                

                                # lấy thông tin người dùng bày tỏ cảm xúc
                                list_like=[]
                                try:
                                    href = article.query_selector('.reactionsBar-link').get_attribute('href')
                                    xpath_expression = f"//a[@href='{href}']"
                                    link_to_click = chromium.page.query_selector(xpath_expression)
                                    
                                    if link_to_click:
                                        link_to_click.click()
                                        chromium.page.wait_for_timeout(2000)
                                        # chromium.page.wait_for_selector("div.overlay-container.is-active")
                                        elements = chromium.page.query_selector_all('li.block-row.block-row--separated')
                                        for e in elements:
                                            chromium.page.evaluate(f'(element) => element.scrollIntoView()', e)
                                            user={}
                                            avatar_element = e.query_selector('.avatar.avatar--s')
                                            user_id = avatar_element.get_attribute('data-user-id')
                                            link_user = self.domain+avatar_element.get_attribute('href')
                                            img = avatar_element.query_selector('img')
                                            if img:
                                                    src = img.get_attribute('src')
                                                    name = img.get_attribute('alt')
                                            else:
                                                src=''
                                                span = avatar_element.query_selector('span')
                                                name = span.inner_text()

                                            div_element = e.query_selector('div.contentRow-extra')
                                            span_element = div_element.query_selector('span')
                                            reaction_id = span_element.get_attribute('data-reaction-id')
                                            time_element = div_element.query_selector('time')
                                            reacted_time = time_element.get_attribute('data-time')
                                            role=''
                                            try:
                                                div_element_2 = e.query_selector('div.contentRow-lesser')
                                                role_element = div_element_2.query_selector('span.userTitle')
                                                role += role_element.inner_text()
                                            except:
                                                pass
                                            try:
                                                div_element_2 = e.query_selector('div.contentRow-lesser')
                                                role_element = div_element_2.query_selector('span.presentation')
                                                role += role_element.inner_text()
                                            except:
                                                pass
                                            
                                            try:
                                                loaction_element = div_element_2.query_selector('a')
                                                link_location = self.domain+loaction_element.get_attribute('href')
                                                location = loaction_element.inner_text() 
                                            except:
                                                link_location=''
                                                location=''
                                                pass

                                            div_element_3 = e.query_selector('div.contentRow-minor')
                                            li_elements = div_element_3.query_selector_all('li')
                                            str_number=''
                                            for li in li_elements:
                                                dl_element= li.query_selector('dl.pairs.pairs--inline')
                                                dd_element = dl_element.query_selector('dd')
                                                number = dd_element.inner_text()+'|'
                                                str_number+=number
                                            user['author'] = name
                                            user['id']= user_id
                                            user['role']= role
                                            user['author_link']= link_user
                                            user['avatar']= self.domain+src
                                            user['location']= location
                                            user['location_link']=link_location
                                            user['km']=int(str_number.split('|')[0].replace(',','')) # số km
                                            user['engine'] = int(str_number.split('|')[1].replace(',','')) # động cơ
                                            # user['points'] = int(str_number.split('|')[2])
                                            user['reacted_time']=int(reacted_time)
                                            if reaction_id=='1':
                                                list_like.append(user)
                                        close_button = chromium.page.query_selector('a.overlay-titleCloser.js-overlayClose')
                                        if close_button:
                                            close_button.click()
                                except:
                                    pass
                                data_crawl['like']= len(list_like)
                                data_crawl['list_like']=list_like

                                data_crawl['out_links']=[]
                                data_crawl['tags']=[]
                                bbWrapper = article.query_selector("div.bbWrapper")
                                image_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.tiff', '.bmp', '.webp', '.heif', '.heic', '.svg',
                                '.raw', '.cr2', '.nef', '.orf', '.sr2']
                                try:
                                    
                                    out_links=article.query_selector_all('div.bbWrapper a:not(blockquote a)')
                                    for o in out_links:
                                        o_href = o.get_attribute('href') if o.get_attribute('href') is not None else ''
                                        if ('/goto/post' not in o_href) and('/members/' not in o_href) and (not any(o_href.endswith(ext) for ext in image_extensions)):
                                            data_crawl['out_links'].append(o_href)
                                        elif ('/members/' in o_href) and (not any(o_href.endswith(ext) for ext in image_extensions)):
                                            data_crawl['tags'].append(o_href)
                                except:
                                    pass
                                data_crawl['out_links'] = [x for x in data_crawl['out_links'] if x is not None and x != '']
                                data_crawl['videos']=[]
                                video_element = bbWrapper.query_selector_all('div.bbMediaWrapper-inner')
                                if video_element:
                                    for v in video_element:
                                        iframes = v.query_selector_all('iframe')
                                        for i in iframes:
                                            video_link=i.get_attribute('src')
                                            data_crawl['videos'].append(video_link)
                                video_element_2 = bbWrapper.query_selector_all('video.videotag')
                                if video_element_2:
                                    for v2 in video_element_2:
                                        src_elements = v2.query_selector_all('source')
                                        for src in src_elements:
                                            s=src.get_attribute('src')
                                            data_crawl['videos'].append(s)
                                    data_crawl['videos'] = [x for x in data_crawl['videos'] if x is not None and x != '']
                                try: 
                                    blockquote = bbWrapper.query_selector_all('blockquote')
                                    data_attributes = len(blockquote)
                                except:
                                    data_attributes=0
                                if data_attributes != 0:
                                    data_sources_list = []
                                    # img_attributes_list = extract_images_within_blockquotes(bbWrapper)
                                    text_after_blockquotes = article.evaluate(
                                                """(article) => {
                                                    const blockquotes = article.querySelectorAll('blockquote');
                                                    let texts = [];
                                                    blockquotes.forEach((bq, index) => {
                                                        let textContent = '';
                                                        let nextNode = bq.nextSibling;
                                                        while(nextNode && (index === blockquotes.length - 1 || nextNode !== blockquotes[index + 1])) {
                                                            if(nextNode.nodeType === Node.TEXT_NODE) {
                                                                textContent += nextNode.textContent.trim();
                                                            } else if (nextNode.tagName === 'BR') {
                                                                textContent += '\\n'; 
                                                            }
                                                            nextNode = nextNode.nextSibling;
                                                        }
                                                        if(textContent) {
                                                            texts.push(textContent);
                                                        }
                                                    });
                                                    return texts;
                                                }""")
                                    data_sources = article.evaluate(
                                                """(article) => {
                                                        const blockquotes = article.querySelectorAll('blockquote');
                                                        return Array.from(blockquotes).map(bq => {
                                                            const bbCodeBlockTitle = bq.querySelector('.bbCodeBlock-title a');
                                                            return bbCodeBlockTitle ? bbCodeBlockTitle.getAttribute('data-content-selector') : null;
                                                        });
                                                    }
                                                """)
                                    data_sources_list.append(data_sources)
                                    
                                    img_attributes_array = article.evaluate(
                                            """(article) => {
                                                const blockquotes = article.querySelectorAll('blockquote');
                                                let srcList = [];
                                                for (let i = 0; i < blockquotes.length; i++) {
                                                    let nextElem = blockquotes[i].nextElementSibling;
                                                    let stopAtNextBlockquote = i + 1 < blockquotes.length ? blockquotes[i + 1] : null;
                                                    while (nextElem && nextElem !== stopAtNextBlockquote) {
                                                        if (nextElem.matches('div') && nextElem.getAttribute('data-src')) {
                                                            srcList.push('https://www.otofun.net'+nextElem.getAttribute('data-src'));
                                                        } 
                                                        else if (nextElem.matches('img') && nextElem.getAttribute('src')) {
                                                            srcList.push(nextElem.getAttribute('src'));
                                                        }
                                                        nextElem = nextElem.nextElementSibling;
                                                    }
                                                }
                                                return srcList;
                                            }""")
                                    #img_attributes_list.append(img_attributes_array)
                                    for i in range(1, len(data_sources)):
                                        if data_sources[i] == '':
                                            data_sources[i] = data_sources[i-1]
                                    for item1, item2 in zip(text_after_blockquotes, data_sources):
                                                id_root_comment=str(item2).replace('#','js-')+'.'
                                                data_crawl['content'] = str(item1).replace('\n\xa0', '').replace("Click to expand...", "")
                                                data_crawl['id']=id_root_comment+id_post
                                                data_crawl['image_url']=img_attributes_array
                                                self.save_data(data_crawl)
                                else:
                                        data_crawl['id']=id_post
                                        txt=''
                                        content_rows = article.query_selector_all("div.bbWrapper")
                                        for content_row in content_rows:
                                            # Lấy và in ra text trong mỗi thẻ div
                                            txt += content_row.inner_text()

                                        user_post = article.query_selector('div.message-userContent.lbContainer.js-lbContainer')
                                        data_crawl['content']= txt.replace('\n\xa0', '').replace("Click to expand...", "")
                                        data_crawl['image_url']=[]
                                        # try:
                                        #     expand_images=article.query_selector_all('div.lbContainer.lbContainer--inline.lbContainer--canZoom')
                                        #     for a in expand_images:
                                        #             img_elements = a.query_selector_all('img')
                                        #             for i in img_elements:
                                        #                 link=i.get_attribute('data-src')
                                        #                 try:
                                        #                     new_link=link.split('?image=')[-1]
                                        #                     clean_link=urllib.parse.unquote(new_link.split('&')[0])
                                        #                     data_crawl['image_url'].append(clean_link)
                                        #                 except:
                                        #                     data_crawl['image_url'].append(link)
                                        #                     pass     
                                        # except:
                                        img_elements = user_post.query_selector_all('img')
                                        for img_element in img_elements:
                                            src = img_element.get_attribute('src')
                                            data_url = img_element.get_attribute('data-url')
                                            try:
                                                src_split=src.split('?image=')[-1]
                                                clean_link=urllib.parse.unquote(src.split('&')[0])
                                                data_crawl['image_url'].append(src_split)
                                            except:
                                                data_crawl['image_url'].append(src)
                                                pass
                                            # pass
                                        data_crawl['image_url'] = [x for x in data_crawl['image_url'] if x is not None and x != '']
                                        self.save_data(data_crawl)
                            except:
                                continue
                        page_num += 1
                    with open('link.txt', 'a', encoding='utf-8') as file:
                        file.write(f'{url}\n')
                    chromium.close()
                except Exception as e:
                    continue
            else:
                    time.sleep(10)
        
            
            
    def save_data(self,data):
        with open('otofun.txt','a',encoding='utf8') as file:
                file.write(f'{data}\n')
                file.close()

    def get_link(self,url):
        # self.link_queue.put('https://xamvn.id/r/khung-hoang-kinh-te-va-sml-chuy-tu-lanh-buon-ba-vi-kiem-chi-40-cu-thang.750879|123|123')
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        midnight_timestamp = int(today.timestamp())
        page_num = 0
        path_crawled='link.txt'
        path_black_link='black_list.txt'
        with open(path_crawled, 'r') as file:
            lines = file.readlines()
        link_crawled=[line.strip() for line in lines]
        with open(path_black_link, 'r') as file:
            line_ = file.readlines()
        black_list=[line.strip() for line in line_]
        chromium2 = ChromiumBrowser(fake=1)
        next_link=''
        while next_link!=None:
            if page_num > 0:
                url = next_link
            try:
                chromium2.page.goto(url,timeout=600000)
                chromium2.page.reload(timeout=600000)
            except:
                chromium2.page.reload(timeout=600000)
                pass
            chromium2.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            try:
                next_link =  chromium2.page.eval_on_selector('a.pageNav-jump.pageNav-jump--next', 'a => a.href')
            except:
                next_link = None
            
            div_elements = chromium2.page.query_selector_all('div.structItemContainer > div')
            for div in div_elements:
                try:
                    li=div.query_selector_all('li.structItem-startDate')[0]
                    a=li.query_selector_all('a')[0]
                    text=a.get_attribute('href')
                    parts = text.rsplit('/', 1)
                    time_element =  li.query_selector('time')
                    time_=int(time_element.get_attribute('data-time'))
                    if len(parts) > 1:
                        href = parts[0] + '/' 
                    cmt_view=div.query_selector_all('div.structItem-cell.structItem-cell--meta')[0]
                    number =cmt_view.inner_text()
                    number= number.split('\n')
                    if href not in link_crawled and href not in black_list and time_ >= midnight_timestamp:
                        print(f'---------->>>>>>>>> Put {href} to Queue')
                        self.link_queue.put(f'{self.domain + href}|{self.convert_unit_to_num(number[1])}|{self.convert_unit_to_num(number[3])}')
                except:
                    continue
            page_num += 1
            time.sleep(2)
        chromium2.close()
    
    # Chuyển chuỗi thời gian thành timestamp
    def txt_to_timestamp(self,txt):
        date_format='%H:%M %d/%m/%Y'
        timezone_str='Asia/Ho_Chi_Minh'
        dt_obj = datetime.strptime(txt, date_format)
        timezone = pytz.timezone(timezone_str)
        dt_obj_localized = timezone.localize(dt_obj)
        timestamp = int(dt_obj_localized.timestamp())
        return timestamp
    
    def convert_unit_to_num(self,txt):
        numbers = (re.findall(r'\d+', txt))[0]
        try:
            words = (re.findall(r'[a-zA-Z]+', txt))[0]
        except:
            words=''
        if words == 'K':
            return int(float(numbers) * 1000)
        elif words == 'M':
            return int(float(numbers) * 1000000)
        elif words == 'B':
            return int(float(numbers) * 1000000000)
        else:
            return int(numbers)

