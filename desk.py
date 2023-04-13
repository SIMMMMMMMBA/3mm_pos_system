
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import telegram
import api_key as ap
import menu as menu
import pickle
import copy
import os
import math
import payment
from datetime import datetime

desk_ui = uic.loadUiType('desk.ui')[0]

class seat_button(QPushButton):
    def __init__(self, parent, name="", title="", payment_list = [], start_time=0, order_list={}, free_list = {}, x=None, y=None):
        super().__init__(title, parent)
        self.parent = parent
        self.name = name
        self.v_order = 0
        self.v_time = 0
        self.start_time = start_time
        self.order_list = copy.deepcopy(order_list)
        self.free_list = copy.deepcopy(free_list)

        if x:
            self.move(x,y)

        self.order_setting()
        self.payment = payment.Payment_Class(self, payment_list)
        self.printing()
        
        
    def mouseMoveEvent(self, e):
        
        if self.parent.pin_ui.isChecked():
            e.ignore()
            return
        drag = QDrag(self)
        
        mime = QMimeData()
        drag.setMimeData(mime)

        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        
        drag.exec(Qt.MoveAction)
        
    def prints(self):
        print(self.name, self.total, self.start_time)
    
    def time_setting(self):
        self.v_time = 0
        if self.start_time == 0:
            return
        delta = datetime.now() - self.start_time
        self.v_time = delta.minute/30*15000
        

    def order_setting(self):
        self.v_order = 0
        for i in self.order_list.keys():
            self.v_order += self.order_list[i] * 18000

    def value_setting(self):
        self.time_setting()
        self.order_setting()
    
    def printing(self):
        strings = self.name + "\n\n"
        cnt = 0
        self.time_setting()
        for i in self.order_list.keys():
            if cnt >=3 :
                break
            elif self.order_list[i]!=0:
                strings = strings + i +' '+ str(self.order_list[i]) +"\n"
                cnt+=1
            
        strings = strings + "\n"
        if self.v_order+self.v_time == 0:
            strings = strings + "빈 좌석\n"
        elif self.start_time == 0:
            strings = strings + "시간 시작 안함\n"
        else:
            strings = strings + self.start_time.strftime("%Y년 %m월 %d일 %H시 %M분") + "\n"
        
        strings = strings + '\n' + str(self.v_order+self.v_time) + '원\n' 
       
        self.setText(strings)
            
    def save(self):
        return {'name': self.name,
                'start_time' : self.start_time,
                'order_list' : self.order_list,
                'free_list' : self.free_list,
                'payment_list' : self.payment.payment_list,
                'x' : self.x(),
                'y' : self.y()}

    def clear(self):
        self.start_time = 0
        self.order_list = {}
        self.free_list = {}
        self.order_setting()
        self.payment.reset()
        self.printing()

class Desk_Class(QMainWindow, desk_ui):
    def __init__(self):
        super( ).__init__( )
        self.initUI()
        self.showMaximized()
        self.show()
        
    def initUI(self):
        self.setupUi(self)
        self.setAcceptDrops(True)
        
        self.seat_list = []
        if os.path.isfile("data/seat_list.pickle"): 
            with open("data/seat_list.pickle", "rb") as json_file:
                for i in pickle.load(json_file):
                    self.create_seat(i)
        self.seat_add.clicked.connect(self.create_seat)
        self.seat_delete.clicked.connect(self.delete_seat)
        self.pin_ui.setCheckable(True)
        self.pin_ui.toggle()
        
        self.seat_move.setCheckable(True)
        self.swap = None
        
    def button_menu(self, seat):
        if self.seat_move.isChecked():
            if self.swap:
                self.swap_seat(self.swap, seat)
                self.swap.toggle()
                self.swap.setCheckable(False)
                self.swap = None
                self.seat_move.toggle()
                self.save()
            else:
                self.swap = seat
                self.swap.setCheckable(True)
                self.swap.toggle()
        else:
            self.hide()
            self.menu = menu.Menu_Class(seat, self)
            self.menu.show()

    def swap_seat(self, seat1, seat2):
        seat1.total, seat2.total = seat2.total, seat1.total 
        seat1.start_time, seat2.start_time = seat2.start_time, seat1.start_time
        seat1.order_list, seat2.order_list = copy.deepcopy(seat2.order_list), copy.deepcopy(seat1.order_list)
        seat1.free_list, seat2.free_list = copy.deepcopy(seat2.free_list), copy.deepcopy(seat1.free_list)
        seat1.printing()
        seat2.printing()

    def dragEnterEvent(self, e):
        if self.pin_ui.isChecked():
            e.ignore()
        else:
            e.accept()
        
    def dropEvent(self, e):
        position = e.pos()
        widget = e.source()
        widget.move(position)
        widget.setDown(False)
        e.accept()
        self.save()
                
    def create_seat(self, default=None):
        idx = len(self.seat_list)
        if default:
            self.seat_list.append(seat_button(self, **default))
            #print(idx, default)
        else :
            self.seat_list.append(seat_button(self, name='좌석'+str(idx)))

        
        self.seat_list[idx].resize(200,300)
        self.seat_list[idx].setCheckable(False)
        self.seat_list[idx].clicked.connect(lambda: self.button_menu(self.seat_list[idx]))
        self.seat_list[idx].show()
        self.save()
        
    def delete_seat(self):
        self.seat_list[-1].deleteLater()
        self.seat_list = self.seat_list[:-1] 
        self.save()
        
    def save(self):
        with open("data/seat_list.pickle", "wb") as f:
            tmp =[i.save() for i in self.seat_list]
            pickle.dump(tmp, f)