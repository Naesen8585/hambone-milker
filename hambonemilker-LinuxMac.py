
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import getpass
import multiprocessing
import random
from webdriverdownloader import ChromeDriverDownloader
import logging


logging.basicConfig(filename='logfile.log',level=logging.WARNING)
SHOW_URL= "https://dlive.tv/ghostpolitics"

gdd=ChromeDriverDownloader()
gdd.download_and_install()

browser_options = Options()
#chrome_options.add_argument('--headless')
width=1920
height=1080
browser_options.add_argument(f'window-size={width}x{height}')
#'/usr/local/bin/chromedriver',
driver = webdriver.Chrome(
         options=browser_options
    )
CURRENTLY_STREAMING=False
spamproc=None
checkproc=None

def check_if_streaming():
    global CURRENTLY_STREAMING
    global spamproc
    global checkproc

    try:
        driver.find_element(By.CSS_SELECTOR, ".position-absolute > img").click()
        print("Hambone is not currently streaming")
        CURRENTLY_STREAMING=False
        try:
            spamproc.terminate()
            checkproc.terminate()
        except Exception as e:
            print("Nothing has started yet, waiting for stream to start...")
            #print(e)
        return False

    except Exception as e2:
        print(e2)
        print("It looks like the hambone is streaming. Starting automated process...")
        return True

def stickerSpam():
    global driver
    while True:
        try:
            print("looking for stickers...")
            randomsticker = random.randint(1,20)
            randomdelay = random.randint(0,5) + 33

            time.sleep(randomdelay)
            #driver.find_element(By.CSS_SELECTOR, "textarea:nth-child(1)").click()
            #driver.find_element(By.CSS_SELECTOR, ".emote-btn > img").click()

            driver.find_element(By.CSS_SELECTOR, ".emote-btn > img").click()
            driver.find_element(By.CSS_SELECTOR, ".flex-align-center:nth-child(2) > .tab-parent").click()
            driver.find_element(By.CSS_SELECTOR, ".emote-item:nth-child("+str(randomsticker)+") > img").click()

            #driver.find_element(By.CSS_SELECTOR, ".v-window-item:nth-child(1) .emote-item:nth-child("+str(randomsticker)+") > img").click()
        except Exception as e:
            print("can't find sticker...")
            print(e)

def signIn(emailaddress,mypassword):
    global driver
    driver.get(SHOW_URL)
    driver.find_element(By.CSS_SELECTOR, ".sign-in-button span").click()
    #emailbox = driver.find_element_by_xpath("//input[@placeholder='Email Address']")
    #passbox=driver.find_element_by_xpath("//input[@placeholder='Password']")
    #emailbox.send_keys(emailaddress)
    #passbox.send_keys(mypassword)
    #driver.find_element(By.CSS_SELECTOR, ".clickable:nth-child(4) > .d-btn-content").click()
    ##Note that I'll find a way to get this to bypass captcha so that it can work headless mode, but for now...
    checking = input("Hit enter on this screen once successfully logged in!")

###!!!---EXPERIMENTAL---!!! DO NOT RELY ON THIS YET
def checkForChest():
    global driver
    while True:
        time.sleep(2)
        try:
            element = driver.find_element(By.LINK_TEXT, "GET THE APP")
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            driver.find_element(By.CSS_SELECTOR, ".width-100 > .d-btn span").click()
            driver.find_element(By.CSS_SELECTOR, ".text-18-medium > span").click()
            driver.find_element(By.CSS_SELECTOR, ".d-btn-content > span > span").click()
            print("GOT THEM LEMS NIBBA")
            driver.refresh()
        except Exception as e:
            print("No lemons found...")
            print(e)


def mainfunction():
    global CURRENTLY_STREAMING
    global spamproc
    global checkproc
    #modify these for future use when we can bypass captcha and auto login
    emailaddress = "dummy"#input("Please enter your email address: >")
    dlivepass="dummy"#getpass.getpass(prompt="Please enter your dlive password (it will not be shown!) >", stream=None)

    signIn(emailaddress,dlivepass)

    while True:
        # only run when hambone is streaming
        time.sleep(3)
        if (check_if_streaming()):
            if not CURRENTLY_STREAMING:
                print("hambone is streaming... starting now")
                # now comes the magic. Begin the spam routine...
                checkproc = multiprocessing.Process(target=checkForChest)
                spamproc = multiprocessing.Process(target=stickerSpam)
                print("starting checkproc")
                checkproc.start()
                print("starting spamproc")
                spamproc.start()
                CURRENTLY_STREAMING = True

if __name__ == '__main__':
    mainfunction()
