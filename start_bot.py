from py3pin.Pinterest import Pinterest
from termcolor import cprint

from os import listdir, mkdir, path

import bot.Parser as parser
import bot.Publisher as publisher

# === Global Variables ===
# --- Pinterest. Pinterest account details for publication
PINTEREST = Pinterest(
    email='email',
    password='password',
    username='usernamee'
)

# This is the board id, more details in the docs folder
BOARD_ID = 'YOURE BOARD_ID'

# How many images are we publishing today? max 50
PINS = 5

# --- Basicdecor
# Parsing https://basicdecor.ru/sovremenoe-iskusstvo/
# Get a list of pages to be parsed
PAGES = parser.get_list_pages()
DIR_FROM_IMAGES = r'bot\data\images_and_data'


def main():
    """ All components of the program start up one by one

    1. the bot checks how many images are still to be published since yesterday
    2. images are stored in the images_and_data folder, if it's not empty, PINS(or 50) of images are published
    3. Bot logs in to the Pinterest site and publishes one picture at a time, then unlogins
    4. If the image is too big, it degrades the quality and reduces the size to 7 megabytes
    5. Then the bot looks at the site basicdecor appeared new paintings, if so, begins to download them one by one
    6. After that it disconnects.

    Publisher.py file - publishes images and information about them on Pinterest. It can work standalone,
    It needs to have the board id and the images_and_data file to store the images and information about the item in
    Product link, name, image link (just in case), price

    File Parser.py - responsible for working with the site basicdecor, to work with other sites or even sections
    it may not work.
    """

    cprint('The bot is running', 'blue')

    # The first part of the code is responsible for parsing images
    if not path.exists(r'bot\data\images_and_data'):
        mkdir(r'bot\data\images_and_data')

    if not listdir(DIR_FROM_IMAGES):
        print("The folder with the images is empty, let's search for new ones")
        parser.get_list_images(PAGES)
        parser.compare_two_files()
        parser.download_images()

    # The second part of the code is responsible for publishing images
    if listdir(DIR_FROM_IMAGES):
        print("The folder with images is not empty, let's start publishing")

        PINTEREST.login()

        publisher.publish(
            dir_path=DIR_FROM_IMAGES,
            pinterest=PINTEREST,
            pins=PINS,
            board_id=BOARD_ID
        )

        PINTEREST.logout()

        print("Bot's done for the day.")

    cprint('The bot has worked successfully and will be disabled', 'blue')


if __name__ == "__main__":
    if BOARD_ID == 'YOURE BOARD_ID':
        print('Enter login password and board number')
    else:
        main()

