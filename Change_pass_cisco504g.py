# скрипт бегает по странице телефона, вбивает логин и пас, потом меняет пас админа.
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

driver = webdriver.Chrome('C:\\Python\\chromedriver.exe') # путь к дравйверу хрома
opts=Options()
def cisco(ip):
    opts.set_headless()
    assert opts.headless # без графического интерфейса.
    browser=Chrome(options=opts)
    browser.get('http://' + ip + '/admin/advanced') # открываем браузер
    system_button = browser.find_element_by_xpath('//*[@id="navSystem"]/a') # ищем элемент по xpath
    # для удобной работы с xpath можно скачать плагин на браузер xpath checker
    system_button.click()
    system_button = browser.find_element_by_id('navSystem')
    system_button.click
    input_form = browser.find_element_by_xpath('//*[@id="System"]/table/tbody/tr[5]/td[4]/input')
    input_form.clear()
    input_form.send_keys('pass')
    input_form.submit()
    # submit_button = browser.find_element_by_xpath('/html/body/form/table/tbody/tr[6]/td[2]/table/tbody/tr/td[2]/input')
    # submit_button.click()
    browser.close()
    print("Пас сменен на " + ip)


myfile=open('C:\\123\\ip2.txt', 'r') # из файлы импортируем айпишники
for ip in myfile:
    try:
        cisco(ip)
    except:
        print("Ошибка на " + ip)
        continue # при ошибке продолжаем
myfile.close()