from playwright.sync_api import sync_playwright

db_link = 'https://www.db.yugioh-card.com/'

with sync_playwright() as p:
  browser = p.chromium.launch(headless=False)
  page = browser.new_page()

  card_name = '백은 성의 라뷰린스'

  page.goto(db_link + "yugiohdb/card_search.action")
  search_box = page.query_selector('xpath=//*[@id="keyword"]')
  search_box.fill(card_name)
  search_button = page.query_selector('//*[@id="submit_area"]/div')
  search_button.click()
  #<input type="hidden" class="link_value" value="/yugiohdb/card_search.action?ope=2&amp;cid=17360">
  page.wait_for_load_state('networkidle')
  hidden_element = page.query_selector('//*[@id="card_list"]/div/input[3]')
  value = hidden_element.evaluate('element => element.getAttribute("value")')
  page.goto(db_link + value)
  
  card_info = {}
  
  h1_text = page.inner_text('//html/body/div[1]/div[2]/div/article/div/div[1]/div[1]/h1')
  span_text = page.inner_text('//html/body/div[1]/div[2]/div/article/div/div[1]/div[1]/h1/span')
    
  card_name = h1_text.replace(span_text, '').strip()
  print(card_name)

  card_info['name'] = card_name
  card_info['attribute']


  
  while(True):
    pass
  print(page.title())
  #browser.close()
  