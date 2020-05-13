import os
import json



def reset():
    '''

        This function is used to delete the configuration files
        created before
        deletes 'accountInfo.json' and
        'videoLinks.txt' from BASE_PATH

    '''
    BASE_PATH = os.getcwd()
    acc_info = os.path.join(BASE_PATH, 'accountInfo.json')
    video_info = os.path.join(BASE_PATH, 'videoLinks.txt')  
    
    if os.path.isfile(video_info):
        os.remove(video_info)

    if os.path.isfile(acc_info):
        os.remove(acc_info)

    help_text = '''
Everything has been reset to Zero.
Try 'ytbot configure' to configure before running again

'''
    print(help_text)





def configure(SETTINGS):
    BASE_PATH = os.getcwd()
    acc_info = os.path.join(BASE_PATH, 'accountInfo.json')
    video_info = os.path.join(BASE_PATH, 'videoLinks.txt')
    accounts = []
    videos = []



    # check if files exist
    if os.path.isfile(acc_info) and os.path.isfile(video_info):
        with open(acc_info) as fa:
            accounts = json.loads(fa.read())
        
        with open(video_info) as fv:
            for line in fv.readlines():
                videos.append(line.strip())
    
    
    # Now we ask for new accounts and video urls
    accounts = askForAccounts(accounts)
    videos = askForVideos(videos)
    
    
    # Now we save credentials and video urls
    with open(acc_info,'w') as fa:
        fa.write(json.dumps(accounts))
    
    with open(video_info,'w') as fv:
        for vid in videos:
            fv.write(vid+'\n')
    
    success = '''Success!!!
Informations are saved. Now to run the bot,
Try 'python3 -m ytbot run' to start the bot'''
    print(success)







def askForAccounts(acc):
    try:
        help_text = '''Hi There! thanks for using this script :)
We need some infos to get going. Give us some disposable 
Google account credentials. Read the Readme.md to know why.
Add atleast 3 accounts. There is no upper limit. 

Press Ctrl+c to stop adding

___________________________________________________________________________
'''
        print(help_text)

        while True:
            newAcc = dict()
            newAcc['username'] = input('Gmail username: ')
            newAcc['pass'] = input('Gmail password: ')      
            acc.append(newAcc)
            print('Account Added!')
            print()
        

    except KeyboardInterrupt as e:
        print('\nExit from google account add Mode!!!')
        return acc


def askForVideos(videos):
    try:
        help_text = '''
Now we need to add youtube video urls. These videos are going to get views

Press Ctrl+c to stop adding

___________________________________________________________________________
'''
        
        print(help_text)
        
        while True:
            newVideo = input('Add yt video Url: ')
            videos.append(newVideo)
            print('Video Added!')
            print()
           
    except KeyboardInterrupt as e:
        print('\nExit from yt video Url Add mode!!!')
        return videos








        
