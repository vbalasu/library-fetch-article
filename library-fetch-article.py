#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys, os
if 'ipykernel_launcher' in sys.argv[0]:
    os.environ['SEARCH_STRING'] = "Tech Wage Inflation Puts Pressure on Companies"
search_string = os.getenv('SEARCH_STRING')
if not search_string:
    sys.exit('Environment variable SEARCH_STRING not defined')


# In[2]:


import uuid
folder = '/tmp/' + str(uuid.uuid4())
os.mkdir(folder)


# In[3]:


from selenium import webdriver


# In[4]:


from selenium.webdriver.common.by import By


# In[5]:


from selenium.webdriver.common.keys import Keys


# In[6]:


# Set options for Save as PDF
chrome_options = webdriver.ChromeOptions()
settings = {"recentDestinations": [{
    "id": "Save as PDF", 
    "origin": "local", "account": ""
}], 
            "selectedDestinationId": "Save as PDF", 
            "version": 2}
import json
prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': folder}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')
#chrome_options.add_argument('--headless')


# In[7]:


driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10) # seconds
driver.get('https://www-proquest-com.rpa.sccl.org/wallstreetjournal?accountid=6247')


# In[8]:


import mysecrets
username = driver.find_element(by=By.CSS_SELECTOR, value='input[name="name"]')
username.send_keys(mysecrets.username)


# In[9]:


pin = driver.find_element(by=By.CSS_SELECTOR, value='input[name="user_pin"]')
pin.send_keys(mysecrets.pin)
pin.send_keys(Keys.RETURN)


# In[10]:


search_bar = driver.find_element(by=By.CSS_SELECTOR, value='textarea#searchTerm')
search_bar.clear()
search_bar.send_keys(search_string)


# In[11]:


search_button = driver.find_element(by=By.CSS_SELECTOR, value='a#expandedSearch')
search_button.click()


# In[12]:


first_result = driver.find_element(by=By.CSS_SELECTOR, value='a#citationDocTitleLink')
first_result.click()


# In[13]:


driver.execute_script('window.print();')


# In[14]:


driver.quit()


# In[15]:


print(folder + '/' + os.listdir(folder)[0])

