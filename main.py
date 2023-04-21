#%%
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import os

from desk import Desk_Class
if __name__ == '__main__':
    #asyncio.run(send_bot('Program booting')) #봇 실행하는 코드
    os.makedirs('data',exist_ok=True)
    app = QApplication(sys.argv)
    myWindow = Desk_Class()
    app.exec_()
    
#%%

