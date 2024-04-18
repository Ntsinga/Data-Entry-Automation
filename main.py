from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import lxml
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
response = requests.get(
    "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A37.8805080917795%2C%22south%22%3A37.669925862938456%2C%22east%22%3A-122.20639315966797%2C%22west%22%3A-122.66026584033203%7D%2C%22mapZoom%22%3A11%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22price%22%3A%7B%22min%22%3Anull%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3Anull%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3Anull%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D",
    headers=headers)
rentals_webpage = response.text

soup = BeautifulSoup(rentals_webpage, "lxml")
print(soup.title)
listing_links = [link.get('href') for link in soup.find_all(name="a", class_="property-card-link")]
prices = [price.getText()[0:6] for price in
          soup.find_all(name='span', class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr")]
addresses = [address.getText() for address in soup.find_all(name='address')]
print(listing_links)
chromedriver_path = r'C:\Users\USER\Dev\chromedriver-win64\chromedriver.exe'

options=webdriver.ChromeOptions()
service=Service(executable_path=chromedriver_path)
options.add_experimental_option("detach",True)
driver=webdriver.Chrome(service=service,options=options)
driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdOjQ_FkTYJY91kYTnmz3-u0owFSFhusoKTstG6ZlH17CJFYA/viewform?usp=sf_link")

for listing in range(len(listing_links)-1):
    address=WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")))
    address.click()
    address.send_keys(addresses[listing])
    price=WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    price.click()
    price.send_keys(prices[listing])
    link=WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    link.click()
    link.send_keys(listing_links[listing])
    submit=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit.click()
    resubmit=WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))
    resubmit.click()

