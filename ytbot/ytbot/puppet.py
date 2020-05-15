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
    SETTINGS['path'] = getExecutablePath()
    
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


# Path = 'C:\\Users\\exploit\\Desktop\\chrome-win\\chrome.exe'
# NotCompleted
async def puppetShow(user,links,SETTINGS):
    try:
        print(user)
        print(links)
        print(SETTINGS)
        await asyncio.sleep(1)
        browser = await launch(
    headless= SETTINGS['headless'],
    executablePath = SETTINGS['path'],
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
    global approvedAccounts
    global triedAccounts
    global pendingAccounts

    if pendingAccounts:
        print('some Accounts are being processed')
    else:
        print('all done!!!')

    print('tried accounts ',triedAccounts)
    print('approved accounts ',approvedAccounts)
    await asyncio.sleep(15)
    while True:
        try:
            await page.goto('https://colab.research.google.com/drive/1Tu7qGmmw3bruw5teb8tnJHmXINchnHC8?usp=sharing',
                                {'waitUntil':'networkidle2'},
                               )
            await asyncio.sleep(2)
            await page.waitForSelector('#toolbar-open-in-playground',{'timeout':160 * 1000})
            await page.click('#toolbar-open-in-playground')
            await asyncio.sleep(5)
            await page.waitForSelector('div.main-content > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.editor.flex.monaco',
                                        {'timeout': 160 *1000}
                                        )
            await page.click('div.main-content > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.editor.flex.monaco')
            await asyncio.sleep(5)
            await page.keyboard.type('''print('hello world')''',{'delay':50})
            await asyncio.sleep(5)

            
            while True:
                # We loop forever here
                try:
                    await page.waitForSelector('#runtime-menu-button')
                    await asyncio.sleep(0.5)
                    await page.click('#runtime-menu-button')
                    await asyncio.sleep(1)
                    await page.waitForSelector('div[command="powerwash-current-vm"]')
                    await asyncio.sleep(0.5)
                    await page.click('div[command="powerwash-current-vm"]')
                    await page.waitForSelector('#ok')
                    await asyncio.sleep(1)
                    await page.click('#ok')
                    await asyncio.sleep(2)
                    await page.waitForSelector('#runtime-menu-button')
                    await asyncio.sleep(1)
                    await page.click('#runtime-menu-button')
                    await asyncio.sleep(2)
                    await page.waitForSelector('div[command="runall"]')
                    await asyncio.sleep(1)
                    await page.click('div[command="runall"]')
                    await asyncio.sleep(2)
                    try:
                        await page.click('#ok')
                    except Exception as e:
                        print(e,' 2nd level')
                    
                    await asyncio.sleep(7 * 60) # This is the view time of each video
                    
                except Exception as e:
                    print(e, ' 1st level')
                    break
                    
        except Exception as e:
            print(e)

# NotCompleted
async def googleLogin(user,page):
    global approvedAccounts
    global triedAccounts
    global pendingAccounts

    triedAccounts += 1
    try:
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

    except Exception as e:
        pendingAccounts.append(user)
        raise e

    print('Logged in and counting...')
    approvedAccounts += 1



# Completed
def stringifyList(given_list):
    stringed_list ='['
    for item in given_list:
        stringed_list += f"'{item}',"
    stringed_list += ']'
    return stringed_list


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
def getExecutablePath():
    BASE_PATH = os.getcwd()
    executable_path = os.path.join(BASE_PATH,'execpath.txt')
    with open(executable_path) as f:
        path = f.read().strip()
        return path

# Completed
def isConfigured():
    BASE_PATH = os.getcwd()
    acc_path = os.path.join(BASE_PATH,'accountInfo.json')
    vid_path = os.path.join(BASE_PATH,'videoLinks.txt')
    executable_path = os.path.join(BASE_PATH,'execpath.txt')
    if os.path.isfile(acc_path) and os.path.isfile(vid_path) and os.path.isfile(executable_path):
        return True
    else:
        return False

