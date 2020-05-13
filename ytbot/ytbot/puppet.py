import asyncio
import os
import json
import time
import pyppeteer

from itertools import cycle
from pyppeteer import launch
from pyppeteer_stealth import stealth


# Global variables needed for all kinds of operations
triedAccounts = 0
approvedAccounts = 0
pendingAccounts = []




# Completed
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

# Completed
async def launchPuppet(SETTINGS):
    print('\nTo stop, Press Ctrl+c ')
    time.sleep(2)
    accounts = getAccounts()
    links = getLinks()
    try:

        tasks = [asyncio.ensure_future(puppetShow(user,links,SETTINGS)) for user in accounts]
        await asyncio.gather(*tasks)



    except KeyboardInterrupt as e:
        help_text = '''
Hey There! Did face any issue while running the app?
Let me Know and I'll try to fix it.
for any additional information, contact me at: 'muhammadfahim010@gmail.com'
Also any kind of feedback would be super encouraging.
Peace Out '''
        print(help_text)
        raise SystemExit('Exit from Bot!')



# NotCompleted
async def puppetShow(user,links,SETTINGS):
    try:
        print(user)
        print(links)
        print(SETTINGS)
        await asyncio.sleep(1)
        browser = await launch(
    headless= SETTINGS['headless'],
    executablePath = 'C:\\Users\\exploit\\Desktop\\chrome-win\\chrome.exe',
    args = ['--no-sandbox','--disable-setuid-sandbox'],
    ignoreHTTPSErrors = True,
    )

        page = await browser.newPage()
        await stealth(page)
        page.setDefaultNavigationTimeout(80*1000)
        await googleLogin(user,page)
        await colabPuppet(links,page)



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



#NotCompleted
async def colabPuppet(links,page):
    print('this is colabPuppet')
    global approvedAccounts
    global triedAccounts
    global pendingAccounts

    if pendingAccounts:
        print('some Accounts are being processed')
    else:
        print('all done!!!')

    print('tried accounts ',triedAccounts)
    print('approved accounts ',approvedAccounts)
    await asyncio.sleep(10)

# NotCompleted
async def googleLogin(user,page):
    global approvedAccounts
    global triedAccounts
    global pendingAccounts

    pendingAccounts.append(user)
    triedAccounts += 1
    await page.goto( 'https://www.stackoverflow.com',
                    {'waitUntil':'networkidle2'},
                   )
    await page.waitForSelector("a[href^='https://stackoverflow.com/users/login?']")
    await page.click("a[href^='https://stackoverflow.com/users/login?']")
    await page.waitForSelector('button[data-provider = "google"]')
    await page.click('button[data-provider = "google"]')
    await page.waitForSelector('input',{'timeout':80*1000})
    await asyncio.sleep(10)
    await page.keyboard.type('\t',{'delay':200})
    await asyncio.sleep(5)
    await page.keyboard.type(user['username'],{'delay':50})
    await asyncio.sleep(5)
    await page.keyboard.type('\n')
    await page.waitForSelector('input[type="password"]',{'timeout':80*1000})
    await page.keyboard.type('\t',{'delay':200})
    await asyncio.sleep(5)
    await page.keyboard.type(user['pass'],{'delay':50})
    await asyncio.sleep(5)
    await page.keyboard.type('\n')
    print('Logged in and counting...')
    approvedAccounts += 1
    pendingAccounts.remove(user)






# Completed
def getAccounts():
    BASE_PATH = os.getcwd()
    acc_path = os.path.join(BASE_PATH,'accountInfo.json')
    with open(acc_path) as f:
        accounts = json.loads(f.read())
        return accounts
# Completed
def getLinks():
    BASE_PATH = os.getcwd()
    vid_path = os.path.join(BASE_PATH,'videoLinks.txt')
    with open(vid_path) as f:
        links = []
        for link in f.readlines():
            links.append(link.strip())
        return links

# Completed
def isConfigured():
    BASE_PATH = os.getcwd()
    acc_path = os.path.join(BASE_PATH,'accountInfo.json')
    vid_path = os.path.join(BASE_PATH,'videoLinks.txt')
    if os.path.isfile(acc_path) and os.path.isfile(vid_path):
        return True
    else:
        return False

