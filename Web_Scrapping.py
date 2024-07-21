from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

webdriver_service = Service("C:\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver.get("https://hprera.nic.in/PublicDashboard")

try:

    wait = WebDriverWait(driver, 120)
    wait.until(EC.presence_of_element_located((By.ID, 'reg-Projects')))
    Details = {}
    for v in range(1,7):
        elements = driver.find_elements(By.XPATH, f'//*[@id="reg-Projects"]/div/div/div[{v}]')
        for e in elements:
            x = e.find_element(By.TAG_NAME,'a')
            x.click()
            wait = WebDriverWait(driver, 120)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="project-menu-html"]/div[2]/div['
                                                                 '1]/div/table/tbody')))
            Data = driver.find_element(By.XPATH,'//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody').text
            #Details={'Project No. 1': None,'Project No. 2': None,'Project No. 3': None,'Project No. 4': None}
            details=[None,None,None,None]
            for i in (Data.split('\n')):
                if 'GSTIN No.' in i:
                    details[0] = i.rstrip('GST Certificate')
                if 'PAN No.' in i :
                    details[1] = i.rstrip('PAN File')
                if 'Name' in i and details[2] == None :
                    details[2] = i
                if 'Permanent Address' in i and details[3] == None :
                    details[3] = i.rstrip('Address Proof')
            Details["Project No."+ str(v)]=details
            driver.find_element(By.XPATH,'//*[@id="modal-data-display-tab_project_main"]/div/div/div[1]/button').click()
    print(Details)

finally:
    driver.quit()
