import asyncio
import click

from .cfg import configure 
from .puppet import run 
from .cfg import reset

# Pass configurations with this dictionary
SETTINGS = dict()



@click.command()
@click.argument('step',default = '')
@click.option('--headless','-h', default=False, is_flag = True)
def main( step, headless):

    SETTINGS['headless'] = headless
    


    if step == 'run':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(SETTINGS))
    
    elif step == 'configure':
        configure(SETTINGS)

    elif step == 'reset':
        reset()

    else:
        print(
        '''Usage: 
            ytbot.py [OPTIONS] [OPTIONS]

            ytbot.py configure                    configure bot for 
                                                  first time

            ytbot.py run                          after configuration
                                                  run the bot
            
            ytbot.py reset                        reset the configuration
                                                  and start anew

            ytbot.py run [--headless][-h]         To run in headless mode!
                                                  Default is headful!!!

''')

        




if __name__=='__main__':
    main()
