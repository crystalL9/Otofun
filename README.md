try:
                        expand_links = chromium.page.query_selector_all(".bbCodeBlock-expandLink.js-expandLink")[0]
                        expand_links.click()
                    except:
                        pass
                    try:
                        spoiler = chromium.page.query_selector_all(".bbCodeSpoiler-button.button")[0]
                        spoiler.click()
                    except:
                        pass