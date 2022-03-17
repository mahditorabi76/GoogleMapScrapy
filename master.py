from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import json
import codecs

def get_link(searchKeywork, executable_path):
    # key_search = 'Best blood labs in Miami'

    # executable_path=r'C:\geckodriver-v0.30.0-win64/chromedriver.exe'
    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en-us')
    profile.update_preferences()
    driver = webdriver.Firefox(firefox_profile=profile, executable_path=r'{}'.format(executable_path))
    driver.get('https://www.google.com/maps/?hl=en')
    time.sleep(5)
    elem = driver.find_element_by_xpath("//div/input[@id ='searchboxinput']")
    elem.send_keys(searchKeywork)
    driver.find_element_by_xpath("//div[2]/div/button").click()

    time.sleep(2)

    # //div/div[@class = 'V0h1Ob-haAclf gd9aEe-LQLjdd OPZbO-KE6vqe']/a
    # //a[@class = 'a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd']

    # list_link = driver.find_elements_by_class_name("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")
    list_link = []
    # len_list_lik = []
    while True:
        try: # Get scroll height
            try:
                xpath_element = "//div[@id='pane']/div/div/div/div/div[4]/div"
                time.sleep(3)
                fBody = driver.find_element_by_xpath(xpath_element)
                Hover = ActionChains(driver).move_to_element(fBody)
                Hover.perform()
                i = 1
                while i < 1000:
                    fBody.send_keys(Keys.ARROW_DOWN)
                    i += 1
            except:
                pass
            time.sleep(2)
            # len_list_lik = len_list_lik + driver.find_elements_by_class_name("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")
            list_link = driver.find_elements_by_class_name("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")
            time.sleep(2)
            with open("uels_file.txt", "+a") as f:
                for i in range(len(list_link)):
                    f.writelines(list_link[i].get_property('href') + "\n")
            try:
                driver.find_element_by_xpath("//div[@class='punXpd']/button[@id='ppdPk-Ej1Yeb-LgbsSe-tJiF1e']/img[@class='hV1iCc-icon']").click()
            except:
                break
        except:
            break
        # list_link = list_link + driver.find_elements_by_class_name("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")

    link_all = []
    with open('uels_file.txt') as f:
        link_all = [x.strip() for x in f.readlines()]
    print("{} links found".format(len(link_all)))
    driver.close()

    # return link_all
    # x = list_link[3].parent.current_url

def crwal_links(number_link, links, searchKeywork, executable_path):
    content = []
    if len(links) < number_link:
        number_link = len(links)

    current_link = []
    for i in range(number_link):
        current_link.append(links[i])


    for link in current_link:
        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages', 'en-us')
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=r'{}'.format(executable_path))
        driver.get(link)
        time.sleep(3)
        title = driver.find_element_by_xpath("//h1[@class= 'x3AX1-LfntMc-header-title-title gm2-headline-5']/span").text
        time.sleep(3)
        driver.find_element_by_xpath("//div/button[@data-value ='Share']").click()
        time.sleep(6)
        driver.find_element_by_xpath("//div/button[@class='s4ghve-AznF2e-ZMv3u-AznF2e NIyLF-haAclf s4ghve-AznF2e-ZMv3u-AznF2e-uqeOfd']").click()
        time.sleep(4)
        driver.find_element_by_xpath("//div/button[@jsaction = 'pane.embedMap.copy']").click()
        MyMap2 = pyperclip.paste()
        MyMap = MyMap2.replace('width="600"', 'width="100%"')
        driver.refresh()
        time.sleep(3)
        try:
            address = driver.find_element_by_xpath("//button[@data-item-id = 'address']").get_attribute(
                'aria-label')[8:]
        except:
            address = ""
        time.sleep(3)
        img_link = driver.find_element_by_xpath(
            "//div[@class = 'F8J9Nb-LfntMc-header-HiaYvf-LfntMc-haAclf d8bJN-LfntMc-HiaYvf']/button/img").get_property(
            "src")
        time.sleep(2)
        try:
            days = driver.find_element_by_xpath(
                "//div[@class = 'OqCZI gm2-body-2 WVXvdc']/div[@class='LJKBpe-open-R86cEd-haAclf t39EBf-Tydcue']").get_attribute(
                'aria-label')
            k_dot = days.find(".")
            days = days[:k_dot]
            days = days.replace(";", "<br>")
            days = days.replace(",", " ")
            days = "\n" + str(days)
        except:
            days = ""
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//img[@alt = 'Copy website']").click()
            website = pyperclip.paste()
        except:
            website = ""
        time.sleep(1)
        try:
            phone = driver.find_element_by_xpath("//button[@data-tooltip='Copy phone number']").get_attribute(
            'aria-label')
            phone = phone[6:]
            phone = phone.replace("-", "")
            phone = phone.replace(" ", "")
        except:
            phone = ""

        content.append([title, website, img_link, days, phone, address, MyMap])

        driver.close()

    html_code = '''
    <h2 class="qrShPb kno-ecr-pt PZPZlf mfMhoc PPT5v hNKfZe" data-dtype="d3ifr" data-local-attribute="d3bn" data-attrid="title" data-ved="2ahUKEwi9vOn339vyAhVTwAIHHezmCN8Q3B0oAHoECAgQAQ">search_master: <a href="link_address_master">Title_master</a></h2>
    <img class="aligncenter size-full wp-image-368" src="img_master" alt="Title_master" width="1024" height="673" />
    <br>
    <br>
    <strong>Hours :  </strong>
    Hours_master
    <br>
    <br>
    <strong>Phone:</strong><a href="tel:tel_master">tel_master</a>
    <br>
    <br>
    <span class="GRkHZd w8qArf"><strong>Address: </strong>Address_master</span>
    <br>
    <br>
    map_master
    <hr size="8" width="30%" color="red">  
    '''

    # search_master
    # Title_master
    # link_address_master
    # img_master
    # Hours_master
    # tel_master
    # Address_master
    # map_master
    # content.append([title, website, img_link, days, phone, address, MyMap])

    with open("log", "+a", encoding= "utf-8") as f:
        for item in content:
            text_html = html_code[:]
            text_html = text_html.replace('search_master', searchKeywork)
            text_html = text_html.replace('Title_master', item[0])
            text_html = text_html.replace('link_address_master', item[1])
            text_html = text_html.replace('img_master', item[2])
            text_html = text_html.replace('Hours_master', item[3])
            text_html = text_html.replace('tel_master', item[4])
            text_html = text_html.replace('Address_master', item[5])
            text_html = text_html.replace('map_master', item[6])

            f.write(text_html)

def crwal_links_range(up, down, links, searchKeywork, executable_path):
    content = []
    # if len(links) < number_link:
    #     number_link = len(links)

    current_link = []
    for i in range(up, down + 1):
        current_link.append(links[i])


    for link in current_link:
        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages', 'en-us')
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=r'{}'.format(executable_path))
        driver.get(link)
        time.sleep(3)
        title = driver.find_element_by_xpath("//h1[@class= 'x3AX1-LfntMc-header-title-title gm2-headline-5']/span").text
        time.sleep(3)
        driver.find_element_by_xpath("//div/button[@data-value ='Share']").click()
        time.sleep(6)
        driver.find_element_by_xpath("//div/button[@class='s4ghve-AznF2e-ZMv3u-AznF2e NIyLF-haAclf s4ghve-AznF2e-ZMv3u-AznF2e-uqeOfd']").click()
        time.sleep(4)
        driver.find_element_by_xpath("//div/button[@jsaction = 'pane.embedMap.copy']").click()
        MyMap2 = pyperclip.paste()
        MyMap = MyMap2.replace('width="600"', 'width="100%"')
        driver.refresh()
        time.sleep(3)
        try:
            address = driver.find_element_by_xpath("//button[@data-item-id = 'address']").get_attribute(
                'aria-label')[8:]
        except:
            address = ""
        time.sleep(3)
        img_link = driver.find_element_by_xpath(
            "//div[@class = 'F8J9Nb-LfntMc-header-HiaYvf-LfntMc-haAclf d8bJN-LfntMc-HiaYvf']/button/img").get_property(
            "src")
        time.sleep(2)
        try:
            days = driver.find_element_by_xpath(
                "//div[@class = 'OqCZI gm2-body-2 WVXvdc']/div[@class='LJKBpe-open-R86cEd-haAclf t39EBf-Tydcue']").get_attribute(
                'aria-label')
            k_dot = days.find(".")
            days = days[:k_dot]
            days = days.replace(";", "<br>")
            days = "\n" + str(days)
        except:
            days = ""
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//img[@alt = 'Copy website']").click()
            website = pyperclip.paste()
        except:
            website = ""
        time.sleep(1)
        try:
            phone = driver.find_element_by_xpath("//button[@data-tooltip='Copy phone number']").get_attribute(
            'aria-label')
            phone = phone[6:]
            phone = phone.replace("-", "")
            phone = phone.replace(" ", "")
        except:
            phone = ""

        content.append([title, website, img_link, days, phone, address, MyMap])

        driver.close()

    html_code = '''
    <h2 class="qrShPb kno-ecr-pt PZPZlf mfMhoc PPT5v hNKfZe" data-dtype="d3ifr" data-local-attribute="d3bn" data-attrid="title" data-ved="2ahUKEwi9vOn339vyAhVTwAIHHezmCN8Q3B0oAHoECAgQAQ">search_master: <a href="link_address_master">Title_master</a></h2>
    <img class="aligncenter size-full wp-image-368" src="img_master" alt="Title_master" width="1024" height="673" />
    <br>
    <br>
    <strong>Hours : </strong>
    Hours_master
    <br>
    <br>
    <strong>Phone:</strong><a href="tel:tel_master">tel_master</a>
    <br>
    <br>
    <span class="GRkHZd w8qArf"><strong>Address: </strong>Address_master</span>
    <br>
    <br>
    map_master
    <hr size="8" width="30%" color="red">  
    '''

    # search_master
    # Title_master
    # link_address_master
    # img_master
    # Hours_master
    # tel_master
    # Address_master
    # map_master
    # content.append([title, website, img_link, days, phone, address, MyMap])
    with open("log", "+a", encoding="utf-8") as f:
        for item in content:
            text_html = html_code[:]
            text_html = text_html.replace('search_master', searchKeywork)
            text_html = text_html.replace('Title_master', item[0])
            text_html = text_html.replace('link_address_master', item[1])
            text_html = text_html.replace('img_master', item[2])
            text_html = text_html.replace('Hours_master', item[3])
            text_html = text_html.replace('tel_master', item[4])
            text_html = text_html.replace('Address_master', item[5])
            text_html = text_html.replace('map_master', item[6])

            f.write(text_html)

if __name__ == '__main__':
    # f = open('config.json',)
    data = json.load(codecs.open('config.json', 'r', 'utf-8-sig'))
    executable_path = data["executable_path"]
    searchKeywork = data["searchKeywork"]
    number_link = data["number_link"]
    read_urls = data["read_urls"]
    range_link = data["range_link"]
    up = data["up"]
    down = data["down"]

    if read_urls == 1:
        get_link(searchKeywork, executable_path)
        input("Press enter and exit ")
        quit()

    link_all = []
    with open('uels_file.txt') as f:
        link_all = [x.strip() for x in f.readlines()]
    if range_link == 0:
        crwal_links(number_link, link_all, searchKeywork, executable_path)
    else:
        crwal_links_range(up, down, link_all, searchKeywork, executable_path)