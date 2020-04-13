import asyncio
import os
import json
import time
import pyppeteer

from itertools import cycle
from pyppeteer import launch
from pyppeteer_stealth import stealth

async def run(SETTINGS):
    if not isConfigured():
        help_text = '''

Bot must be configured before using it!
Try 'bot.py configure' and follow instruction. Then after the 
configuration is complete, run the bot with 'bot.py run'     

'''
        print(help_text)
        raise SystemExit('Bot must be configured before use!')
    else:
        await launchPuppet(SETTINGS)


async def launchPuppet(SETTINGS):
    print('\nTo stop, Press Ctrl+c ')
    time.sleep(2)
    accounts = getAccounts()
    links = getLinks()
    try:
        for user in cycle(accounts):
            await puppetShow(user, links, SETTINGS)

    except KeyboardInterrupt as e:
        help_text = '''
Hey There! Did face any issue while running the app?
Let me Know and I'll try to fix it.
for any additional information, contact me at: 'muhammadfahim010@gmail.com'
Also any kind of feedback would be super encouraging.
Peace Out '''
        print(help_text)
        raise SystemExit('Exit from Bot!')

async def puppetShow(user,links,SETTINGS):
    try:
        print(user)
        print(links)
        print(SETTINGS)
        time.sleep(1)
        browser = await launch(
    headless= SETTINGS['headless'],
    executablePath = 'C:\\Users\\exploit\\Desktop\\chrome-win\\chrome.exe',
    args = ['--no-sandbox','--disable-setuid-sandbox'],
    ignoreHTTPSErrors = True,
    )
        
        page = await browser.newPage()
        await stealth(page)
        time.sleep(2)

        page.setDefaultNavigationTimeout(80*1000)
        await page.goto('https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/',
                        {'waitUntil':'networkidle2'}
                        )

        time.sleep(3)
        await page.keyboard.type('\t',{'delay':200})
        await page.keyboard.type(user['username'],{'delay':50})
        time.sleep(10)
    



        time.sleep(4)

# using the next line will cause the browser to hang and not close 
#        await page.close()
        
        await browser.close()
    
    except KeyboardInterrupt:
        try:
            await browser.close()
            raise SystemExit('Exiting from browser')
        except:
            print('already closed')
    
    except pyppeteer.errors.TimeoutError as e:
        print(str(e))
        try:
            await browser.close()
        except:
            print('browser already closed')

    except RuntimeError as e:
        print(str(e))
        try:
            await browser.close()
            raise SystemExit('Exiting from browser')
        
        except Exception as e:
            print('did not close browser second time')
    
   # except Exception as e:
  #      print(str(e))
 #       print('unknown exception')
#        raise SystemExit

def getAccounts():
    BASE_PATH = os.getcwd()
    acc_path = os.path.join(BASE_PATH,'accountInfo.json')    
    with open(acc_path) as f:
        accounts = json.loads(f.read())
        return accounts

def getLinks():
    BASE_PATH = os.getcwd()    
    vid_path = os.path.join(BASE_PATH,'videoLinks.txt')
    with open(vid_path) as f:
        links = []
        for link in f.readlines():
            links.append(link.strip())
        return links


def isConfigured():
    BASE_PATH = os.getcwd()
    acc_path = os.path.join(BASE_PATH,'accountInfo.json')
    vid_path = os.path.join(BASE_PATH,'videoLinks.txt')
    if os.path.isfile(acc_path) and os.path.isfile(vid_path):
        return True
    else:
        return False
    
