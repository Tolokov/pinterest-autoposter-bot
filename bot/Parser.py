from requests import get
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import lxml
from os import mkdir, path, remove
from termcolor import cprint


def get_user_agent():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return headers


def get_list_pages():
    """We want to get the number of pages on the site
    basicdecor in the art for parsing and automation
    """
    link = 'https://basicdecor.ru/sovremenoe-iskusstvo/'
    response = get(url=link, headers=get_user_agent())
    soup = bs(response.content, 'lxml')
    last_page = soup.find('li', class_='pagination__item pagination__last')
    return int(last_page.a['data-page'])


# https://basicdecor.ru/
# The bot goes through all the pages of the gallery and collects links to all the published paintings.
# Save the resulting list to the file new_list_links.txt
def get_list_images(pages):

    print('The program starts collecting data from the basicdecor.ru site')
    list_links = list()
    count = 0

    for num_page in range(1, pages + 1):

        response = get(
            url=f'https://basicdecor.ru/sovremenoe-iskusstvo/?page={num_page}',
            headers=get_user_agent()
        )

        soup = bs(response.content, 'lxml')

        # If the data collection is not correct, the error is probably here:
        list_main = soup.find('div', class_='product-list--main-list')
        for i in list_main.find_all(class_='product-card__title_bm'):
            count += 1
            list_links.append(i.get('href'))
        print('.', end='')

    print(f'\nThe program collected {count} links to pages with pictures')

    with open(r'bot\data\new_list_links.txt', 'w') as file:
        file.write('\n'.join(list_links))
        file.write('\n')


# The function compares the contents of two files:
# 1. A list of all the pictures in the gallery.
# 2. A list of all the pictures published on Pinterest
# (stored in the history.txt file)
# The difference between the second and the first file will be
# the pictures that have not yet been published on Pinterest
def compare_two_files():
    # These variables are hardwired into the whole code and have to be registered manually in each function
    # You can change them, but you don't have to
    history_file = r'bot\data\history.txt'
    new_list_links = r'bot\data\new_list_links.txt'

    # Check if both files exist
    if not path.exists(new_list_links):
        assert FileNotFoundError(
            'The first part of the code did not work correctly, '
            'the file with the list of new images is empty')

    if not path.exists(history_file):
        old_file = open(history_file, "w")
        old_file.write("\n")
        old_file.close()
        print('Saved history is empty, a new empty file was created')

    # Read two files into memory and perform algorithmic operations:
    with open(history_file, 'r') as old_file:
        history = set(old_file.read().split('\n'))
    with open(new_list_links, 'r') as new_file:
        new_history = set(new_file.read().split('\n'))
    diff = new_history - history

    # The system checks how many new paintings are published on Basicdecor
    if len(diff) == 0:
        cprint('No new paintings found, the program stops working', 'blue')
        remove(new_list_links)  # Delete the file with the list of changes
        exit()
    else:
        print(f'Found {len(diff)} new items:')
        print(diff)

        # If new paintings are found, a file is created in which the list of maps for download is stored
        with open(r'bot\data\temp_list.txt', 'w') as file:
            file.write('\n'.join(tuple(diff)))
            file.write('\n')

        # print('A file temp_list.txt was created to store a temporary list of links')


# https://basicdecor.ru/
# Go through each picture and get all the information we need
# a new directory will appear with the picture and an additional information file
def download_images():

    print('Starting to download images!')

    # This part of the code opens a temporary file and goes through each line
    with open(r'bot\data\temp_list.txt', 'r') as file:

        count_links = 0

        for link in file:
            count_links += 1

            link = link.replace('\n', '')

            # Get the link and send a request to the gallery server
            url = f"https://basicdecor.ru{link}"
            print('.', end='')
            response = get(url=url, headers=get_user_agent())
            soup = bs(response.content, 'lxml')

            # It was decided to use the json script, since it changes less often than the page
            content_main = soup.find_all('script', type='application/ld+json')
            content = content_main[0]  # The data we need
            tmp_dict = {'url': f'{url}'}

            for i, value in enumerate(content.text.strip().split('\n')):

                # If at this stage an error occurs, most likely the API of
                # the site has changed and you need to fix some of the code:
                # print(i, value)
                if i in (4, 5, 12):
                    if "name" in value:
                        row = value.split(':')
                        tmp_dict['name'] = row[1].replace('\"', '').strip(',').strip()

                    elif "image" in value:
                        row = value.split(':')
                        tmp_dict['image'] = 'https:' + row[2].replace('\"', '')

                    elif "price" in value:
                        row = value.split(':')
                        tmp_dict['price'] = row[1][:len(row[1]) - 1].strip(',').replace('\"', '').strip()

                    else:
                        print(i, value)
                        raise IndexError

            try:
                save_image(num_img=count_links, data=tmp_dict)

            except Exception('ERROR') as e:
                print(e, tmp_dict)

            tmp_dict.clear()
            # break  # Set if we want to work with only one image
    print(f'\nDownload {count_links} images')
    update_history()


def update_history():
    """Update file history"""
    history_file = r'bot\data\history.txt'
    temp_list_links = r'bot\data\temp_list.txt'
    new_list_links = r'bot\data\new_list_links.txt'

    with open(history_file, 'a') as h_file:
        with open(temp_list_links, 'r') as t_file:
            h_file.write(t_file.read())

    remove(new_list_links)  # Delete the file with the list of changes
    remove(temp_list_links)  # Deleting a temporary file

    print('The history of downloaded pictures has been updated')


def save_image(num_img: int, data: dict):
    """Save images"""
    path_to_img = data['image'].strip(',')
    form = path_to_img.split('.')[-1:][0]
    response = get(url=path_to_img, headers=get_user_agent())
    if not path.exists(r'bot\data\images_and_data'):
        mkdir(r'bot\data\images_and_data')

    try:
        mkdir(rf'bot\data\images_and_data\{num_img}')
    except FileExistsError as fe:
        mkdir(rf'bot\data\images_and_data\_{num_img}')
        print(fe, 'a new name will be created')

    with open(rf'bot\data\images_and_data\{num_img}\img.{form}', 'wb') as file_image:
        file_image.write(response.content)

    # save meta data
    with open(rf'bot\data\images_and_data\{num_img}\data.txt', "w", encoding="utf-8") as file:
        for line in data.values():
            file.write(line + '\n')


if __name__ == '__main__':
    print(get_list_pages())
