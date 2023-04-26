import time
import os
import pyautogui
from PIL import Image
from telegram import Bot
import telegram
import asyncio
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

with open("telegram_api.txt", "r") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    channel_id = lines[1].strip()

async def send_bot_photo(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token = api_key)

    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a file
    screenshot_path = 'screenshot.png'
    screenshot.save(screenshot_path)

    with open(screenshot_path, 'rb') as f:
        await bot.send_photo(chat_id=channel_id, photo=f, write_timeout=60)

    os.remove(screenshot_path)

# Loop indefinitely and take a screenshot every minute

auto_ui = uic.loadUiType('telegram_sendphoto.ui')[0]
class auto(QMainWindow, auto_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        
        self.start.clicked.connect(self.start_timer)
        self.end.clicked.connect(self.end_timer)
        if self.start.isChecked():
            self.start_timer()
        self.end.setDisabled(True)

    def start_timer(self):
        self.start.toggle()
        self.timer = QTimer(self)                   # timer 변수에 QTimer 할당
        self.telegram_sendphoto()
        self.timer.setInterval(1000*60*int(self.time.text()))    # 1초마다 timeout 발생
        self.timer.timeout.connect(self.telegram_sendphoto)    # start time out시 연결할 함수
        self.timer.start()
        self.end.setDisabled(False)
        self.start.setDisabled(True)

    def end_timer(self):
        self.timer.stop()
        self.start.setDisabled(False)
        self.end.setDisabled(True)

    def telegram_sendphoto(self):
        asyncio.run(send_bot_photo())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = auto()
    app.exec_()