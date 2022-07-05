from py3pin.Pinterest import Pinterest
from os import scandir, path, remove
from shutil import rmtree
from PIL import Image


def publish(dir_path, pinterest, pins, board_id):
    """Call it when we want to publish images on Pinterest"""

    count = 0
    with scandir(r'bot\data\images_and_data') as dir:
        for entry in dir:

            if pins < 1:
                break
            pins -= 1

            with open(rf'{dir_path}\{entry.name}\data.txt', 'r', encoding="utf-8") as file:

                if path.exists(rf'{dir_path}\{entry.name}\img.jpg'):
                    form = 'jpg'
                elif path.exists(rf'{dir_path}\{entry.name}\img.png'):
                    form = 'png'
                else:
                    form = 'jpeg'

                image_file = rf'{dir_path}\{entry.name}\img.{form}'

                link_to_product, title, link_to_image, price = file

                if 'Юлия Болдовская' in title or 'Болдовская Юлия' in title:
                    pins += 1
                    file.close()
                    rmtree(rf'{dir_path}\{entry.name}', ignore_errors=True)
                    continue

                # print(link_to_product, title, link_to_image, price)

                # If the image is larger than 7 megabytes, then compress it
                sizer(image_file)

            try:
                # Uploading an image to Pinterest
                title = title.replace("\n", "")
                pinterest.upload_pin(
                    board_id=board_id,
                    image_file=image_file,
                    description=f'{title}\n buy from the online store: basicdecor.ru for {price} RUR.',
                    title=title,
                    section_id=None,
                    link=link_to_product
                )
                count += 1
                print(f'Image #{count}: {title} uploaded')

            except Exception as ex:
                print(ex)
                continue
            else:
                # Delete unnecessary folder with image and data file
                rmtree(rf'{dir_path}\{entry.name}', ignore_errors=True)

    print(f'Uploaded {count} publications')


# The function compresses the image if it is too large
def sizer(path_to_img):
    """max 7 mb"""
    if path.getsize(path_to_img) > 7_000_000:
        if path.getsize(path_to_img) > 15_000_000:
            q = 40
        else:
            q = 95
        try:
            print('The image is too big, try to make it smaller')
            img = Image.open(path_to_img)
            w, h = img.size
            img = img.resize((w, h))
            img.save(path_to_img, quality=q)
            print('Image reduced')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pass


