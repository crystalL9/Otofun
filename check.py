import requests
proxies = {
                'http': '192.168.143.101:4005',
                'https': '192.168.143.101:4005'
            }
video_id='7206165588794674458'
# headers = {
#                 "authority": "www.tiktok.com",
#                 "Accept-Encoding": "gzip, deflate, br, zstd",
#                 "Connection": "keep-alive",
#                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
#                 'referer': f'https://www.tiktok.com/@giaidapthacmac/photo/{video_id}',
#                 "authority": "www.tiktok.com"
#             }
                # params = {
                #             'msToken': '',
                #             'X-Bogus': 'DFSzswVOIPJANVbotLWIlSRhGwlU',
                #             '_signature': '_02B4Z6wo00001p4ZIYQAAIDC8H0X6KeCtiaeGSUAAMKBf2',
                # params=encoder(params, safe = '=')
                #             }

res = requests.get(f"https://m.tiktok.com/api/item/detail/?WebIdLastTime=1710320873&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F122.0.0.0%20Safari%2F537.36&channel=tiktok_web&clientABVersions=70508271&clientABVersions=70537619&clientABVersions=71681250&clientABVersions=71767681&clientABVersions=71818227&clientABVersions=71881870&clientABVersions=71907464&clientABVersions=71930325&clientABVersions=71937165&clientABVersions=71961453&clientABVersions=71996341&clientABVersions=72014265&clientABVersions=72019410&clientABVersions=72042542&clientABVersions=72072742&clientABVersions=72076224&clientABVersions=70138197&clientABVersions=70156809&clientABVersions=70405643&clientABVersions=71057832&clientABVersions=71200802&clientABVersions=71381811&clientABVersions=71516509&clientABVersions=71691165&clientABVersions=71803300&clientABVersions=71957976&clientABVersions=71962127&clientABVersions=71971888&cookie_enabled=true&coverFormat=2&device_id=7345772043566761478&device_platform=web_pc&focus_state=false&from_page=user&history_len=3&is_fullscreen=false&is_page_visible=true&itemId=7321247711137746194&language=en&os=windows&priority_region=VN&referer=&region=VN&screen_height=1080&screen_width=1920&tz_name=Asia%2FSaigon&verifyFp=verify_ltpkwbgk_OEfEfB8A_J6b7_4LA9_Aa5C_RpdVu8cqsqTN&webcast_language=en&msToken=mtiTdlTjZqMxNEVmHbbu3z843J0MDdRkwW99xJT9rGaPl01O3ng0zuv1PudaMyc-FANde4MDDQq42gBxZhjBElnnULyu6aC6dvTo5vxUNDqz0S5hzKpZbhB5GMGG3AE5TJZSZ5Z_xIE1eONA&X-Bogus=DFSzswVOlAsANVbotLWZSuRhGwWV&_signature=_02B4Z6wo00001F6ePNgAAIDAMPoKth.62nRenjhAAHJb26" )
html = res.text