
Bot to post images from Basicdecor to the Punterest board (Python 3.10)

---

WARNING!!! The first run will download about 7gb of images

At 2500 images, posts will take 50 days to download

Running on windows:
1. press win+r combination, type 'cmd', execute. This will open a command line window.
2. go to the directory with the virtual environment, for example: cd C:\Users\Python Dev\Desktop\bot_basicdecor v3\VENV\Scripts
Or create a new one with command python -m venv venv, then in the Scripts directory execute command activate
3. Climb two directories above by executing the command 'cd...' twice or cd C:\Users\Python Dev\Desktop\bot_basicdecor v3\
4. Execute the command 'start_bot.py', the bot will start

---

1. the bot sees how many images still have to be published since yesterday
2. images are stored in images_and_data folder, if it is not empty, bot will publish PINS(or 50) images
3. Bot logs in to the Pinterest site and publishes one picture at a time, then unlogins
4. If the image is too big, it degrades the quality and reduces the size to 7 megabytes
5. Then the bot looks at the site basicdecor appeared new paintings, if so, begins to download them one by one
6. After that it disconnects.

Publisher.py file - publishes images and information about them on Pinterest. It can work standalone,
It needs to have the board id and the images_and_data file to store the images and information about the item in
Product link, name, image link (just in case), price

File Parser.py - responsible for working with the site basicdecor, to work with other sites or even sections
it may not work.

To work you need to install the browser chrome:
https://www.google.ru/chrome/

---

If you want to change the description of the pin, you can do it on line 38 in the file Publisher.py

    description=f'{title}\n buy at online store: basicdecor.ru for {price} rubles', # description

---
If an error occurs 

    selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary

You need to install chrome browser
Read more about the error on the sites:
https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
https://stackoverflow.com/questions/50138615/webdriverexception-unknown-error-cannot-find-chrome-binary-error-with-selenium

---

If an error occurs:

    429 Client Error: Too Many Requests for url: https://www.pinterest.com/resource/PinResource/create/
    0 uploads

So the maximum number of images uploaded so far

---

If an error occurs:

    0 uploaded publications
    401 Client Error: Unauthorized for url: https://www.pinterest.com/upload-image/
    requests.exceptions.HTTPError: 401 Client Error:

So the bot didn't correctly terminate the previous Pinterest session,
You need to disable it manually, more info in the 'error 401' image

---

If an error occurred:
    
    TimeoutError: [WinError 10060] Attempting to establish a connection was unsuccessful because there was 
    computer did not respond in the time required, or an already established connection was lost due to an incorrect response from the other computer. 
    connection was broken because of an incorrect response from the already connected computer


It means that the connection was interrupted during the image acquisition or the server severed the connection forcibly.
This happens when a lot of similar requests to the site were sent

The work of bot will stop and history of downloaded images will not be updated.
You have to start downloading again - to do that, delete the content of the images_and_data folder or 
entire folder and run the bot again.

You may need to change IP address or use proxy to send requests.
It worked for me once during nonstop testing of basicdecor site
You could add a construct:

    from time import sleep
    sleep(2) 

In Parser.py, line 37. But that's not likely to be needed.


---

If there is an error:

    socket.gaierror: [Errno 11001] getaddrinfo failed

It means there's no internet or the ports for going online are disconnected.
