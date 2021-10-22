from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

# CONSTANTS
CHROME_DRIVER_PATH = "C:/Users/ccesports2/Development/chromedriver"
FORM_LINK = "https://forms.gle/Ai4aDtxfG5nfHRud7"
ZILLOW_LINK = "https://www.zillow.com/hi/1-_beds/1.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
              "%22usersSearchTerm%22%3A%22hawaii%22%2C%22mapBounds%22%3A%7B%22west%22%3A-160.7401149765625%2C%22east" \
              "%22%3A-154.3131130234375%2C%22south%22%3A18.423029653379047%2C%22north%22%3A22.711041620136577%7D%2C" \
              "%22regionSelection%22%3A%5B%7B%22regionId%22%3A18%2C%22regionType%22%3A2%7D%5D%2C%22isMapVisible%22" \
              "%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A3000000%2C%22max%22%3A10000000%7D%2C" \
              "%22mp%22%3A%7B%22min%22%3A7286%2C%22max%22%3A24288%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22beds" \
              "%22%3A%7B%22min%22%3A1%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C" \
              "%22mapZoom%22%3A8%7D "

# ACCESS ZILLOW AND MAKE SOUP
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                  " like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
response = requests.get(ZILLOW_LINK, headers=headers)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

# ACCESS INDIVIDUAL ELEMENTS
addr_elements = soup.find_all(class_="list-card-addr")
addr_list = [addr.getText() for addr in addr_elements]

price_elements = soup.find_all(class_="list-card-price")
price_list = [price.getText() for price in price_elements]

link_elements = soup.find_all(class_="list-card-link")
link_list = []
for x in range(len(link_elements)):
    try:
        link_list.append(link_elements[x].attrs["href"])
    except KeyError:
        link_list.append("No link")

link_list_final = []
[link_list_final.append(link) for link in link_list if link not in link_list_final]
print(link_list_final)
# PUT INFO INTO FORM WITH SELENIUM

driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(FORM_LINK)
driver.maximize_window()

for x in range (len(addr_list)):
    time.sleep(3)
    address = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(f"{addr_list[x]}")

    price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(f"{price_list[x]}")

    link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(f"{link_list_final[x]}")

    submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    submit.click()

    time.sleep(2)

    another = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another.click()