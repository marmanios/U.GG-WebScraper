from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

def getCounters(raw_counters):
    counter_names = []
    #find top 5 counters
    begin = 0
    fin = len(raw_counters) - 1
    for counter_champ in raw_counters:
        if begin != fin:
            href = counter_champ['href']
            start_num = href.find('s/') + 2
            end_num = href.find('/build')
            counter_name = href[start_num:end_num]
            counter_names.append(counter_name)
        begin += 1        
    return counter_names

    
opt = Options()
opt.headless = True
opt.add_argument("window-size=1920x1080")
opt.binary_location = "D:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_driver_binary = "D:\chromedriver92\chromedriver.exe"
driver = webdriver.Chrome(r"C:\Users\Maged Armanios\Documents\Chrome driver\chromedriver.exe", options=opt) # Modify based on where ur file is (pre sure u need to download that online as a zip
driver.get("https://u.gg/lol/tier-list?rank=overall.html")
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(0.1) 

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

soup_file=driver.page_source
soup = BeautifulSoup(soup_file, "html.parser")
driver.quit()

all_rows = soup.find_all('div', attrs={'class':'rt-tr-group'})
if len(all_rows) != 229:
    print("Update Row num to")
    print(len(all_rows))
    
else:
    counter = 0
    for row in all_rows:
        cells = row.div.contents
        role = cells[1].img['alt']
        champ_name = cells[2].text
        win_rate = cells[4].text
        pick_rate = cells[5].text 
        ban_rate = cells[6].text

        #find top 5 counters
        counter_names = getCounters(cells[7].div.find_all('a'))
        counter+= 1

        # All data is found at this point
        print(str(counter) + ". " + champ_name + " as " + role + ". Pick Rate: " + str(pick_rate) + ". Win Rate: " + str(win_rate) + ", Ban Rate: " + str(ban_rate) + ". Counters: " , end = '')
        print(*counter_names,   sep = ', ', end = '')
        print('.')

