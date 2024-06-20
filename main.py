import re
import random
import time
from collections import deque

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

opt = webdriver.ChromeOptions()
opt.add_argument("--disable-popup-blocking")

url = "https://monkeytype.com/"

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opt)

driver.get(url)

time.sleep(2)
try:
    driver.find_element(By.CLASS_NAME, "rejectAll").click()
except NoSuchElementException:
    print("Element not found")

try:
    driver.find_element(By.ID, "words").click()
except NoSuchElementException:
    print("Element not found 2")
    
time.sleep(2)

def type_word(word):
    body = driver.find_element(By.TAG_NAME, 'body')
    actions = ActionChains(driver)
    actions.send_keys(word + " ")
    actions.perform()

k = 10
last_k_sequences = deque(maxlen=k)

while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    word_elements = soup.find_all("div", class_="word")
    words = [element.get_text() for element in word_elements]
    
    current_sequence = " ".join(words)
    
    if current_sequence not in last_k_sequences:
        for word in words:
            type_word(word)
        last_k_sequences.append(current_sequence)
    else:
        print(f"Skipping sequence: {current_sequence}")
    