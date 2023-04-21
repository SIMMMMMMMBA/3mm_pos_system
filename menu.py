
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import telegram
import api_key as ap
import asyncio
import pickle
import copy
import os
import math
import pandas as pd 
from datetime import datetime

import desk
import payment

class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

menu_ui = uic.loadUiType('menu.ui')[0]
class Menu_Class(QMainWindow, menu_ui):
    def __init__(self, seat, parent):
        super( ).__init__()
        self.seat = seat
        self.parent = parent
            
        self.initUI()
        self.showMaximized()
        self.seat_dic  = {}
            
    def clicked_ui(self):
        self.menu1.clicked.connect(lambda : self.order(0))
        self.menu2.clicked.connect(lambda : self.order(1))
        self.menu3.clicked.connect(lambda : self.order(2))
        self.menu4.clicked.connect(lambda : self.order(3))
        self.menu5.clicked.connect(lambda : self.order(4))
        self.menu6.clicked.connect(lambda : self.order(5))
        self.menu7.clicked.connect(lambda : self.order(6))
        self.menu8.clicked.connect(lambda : self.order(7))
        self.menu9.clicked.connect(lambda : self.order(8))
        self.menu10.clicked.connect(lambda : self.order(9))
        self.menu11.clicked.connect(lambda : self.order(10))
        self.menu12.clicked.connect(lambda : self.order(11))
        self.menu13.clicked.connect(lambda : self.order(12))
        self.menu14.clicked.connect(lambda : self.order(13))
        self.menu15.clicked.connect(lambda : self.order(14))
        self.menu16.clicked.connect(lambda : self.order(15))
        self.menu17.clicked.connect(lambda : self.order(16))
        self.menu18.clicked.connect(lambda : self.order(17))
        self.menu19.clicked.connect(lambda : self.order(18))
        self.menu20.clicked.connect(lambda : self.order(19))
        self.start.clicked.connect(self.starting_time)
        self.end.clicked.connect(self.ending_time)
        if self.seat.start_time !=0:
            self.start.setDisabled(True)
        else:
            self.end.setDisabled(True)
            
        self.order_table.setSelectionBehavior(QTableView.SelectRows)
        self.order_table.clicked.connect(self.blocking_service)

        self.order_delete.clicked.connect(self.order_delete_one)
        self.order_add.clicked.connect(self.order_add_one)
        self.order_service.clicked.connect(self.order_free_one)
        
    def starting_time(self):
        self.start.setDisabled(True)
        self.seat.start_time = datetime.now()
        self.end.setDisabled(False)
        asyncio.run(send_bot(self.seat.name + self.seat.start_time.strftime(" %Y년 %m월 %d일 %H시 %M분 입실")))
        self.parent.save()
        self.parent.time_setting()
        
    def ending_time(self):
        self.start.setDisabled(False)
        end_time = datetime.now()
        self.end.setDisabled(True)
        asyncio.run(send_bot(self.seat.name + end_time.strftime(" %Y년 %m월 %d일 %H시 %M분 퇴실")))
        self.seat.start_time = 0
        self.parent.save()        

    def initUI(self):
        self.setupUi(self)
        self.exit.clicked.connect(self.Home)
        
        #메뉴 주문 관련
        self.menu_list = ['야마자키 12', '토끼', '달모어 12', '달모어 12 쉐리', '달모어 15', '달모어 18', '달모어 21', '달모어 25', '달모어 30', '임시용 1', '임시용 2','임시용 3','임시용 4',
                          '임시용 11', '임시용 12','임시용 13','임시용 14', '임시용 15', '임시용 215','임시용 311','임시용 41', '임시용 11', '임시용 21','임시용 31','임시용 41',
                          '스프링뱅크 12', '스프링뱅크 15', '스프링뱅크 18', '스프링뱅크 21', '스프링뱅크 25']
        self.value = [18000]*len(self.menu_list)
        
        self.menu_list.sort()
        self.page = 0
        self.max_page = math.ceil(len(self.menu_list)/20.0)-1
        self.menu_buttons = [self.menu1,self.menu2,self.menu3,self.menu4,
                             self.menu5,self.menu6,self.menu7,self.menu8,
                             self.menu9,self.menu10,self.menu11,self.menu12,
                             self.menu13,self.menu14,self.menu15,self.menu16,
                             self.menu17,self.menu18,self.menu19,self.menu20]
        self.clicked_ui()
        self.order_table_ui()
        
        self.set_menu_text(init = True)
        self.left.clicked.connect(self.menu_left)
        self.right.clicked.connect(self.menu_right)
        self.payment.clicked.connect(self.click_payment)
        
        #start 관련

    def clear_seat(self):
        self.seat.clear()
        self.Home()

        #결제 관련
    def click_payment(self):
        self.seat.value_setting()
        self.seat.payment.payment_print()
        self.seat.payment.exec_()
        self.payment_print()
        self.parent.save()
        if self.seat.payment.result:
            self.clear_seat()

    def Home(self):
        self.close()
        self.seat.printing()
        self.parent.show()
    
    def order(self, i):
        strings = self.menu_list[self.page*20+i]
        if strings in self.seat.order_list :
            self.seat.order_list[strings] +=1
        else:
            self.seat.order_list[strings] = 1
        self.order_table_ui()
    
    def blocking_service(self):
        x = self.order_table.selectedIndexes()
        if x:
            if len(self.seat.order_list) > x[0].row():
                self.order_service.setDisabled(False)
            else:
                self.order_service.setDisabled(True)
                
    def order_delete_one(self):
        x = self.order_table.selectedIndexes()
        if x:
            strs = self.order_table.model().data(x[0],Qt.DisplayRole)
            if len(self.seat.order_list) > x[0].row():
                self.seat.order_list[strs] -= 1
                self.order_table_ui()
                
                if self.seat.order_list[strs] == 0:
                    del self.seat.order_list[strs]
                else:
                    self.order_table.selectRow(x[0].row())
            else :
                self.seat.free_list[strs] -= 1
                self.order_table_ui()
                if self.seat.free_list[strs] == 0:
                    del self.seat.free_list[strs]
                else:
                    self.order_table.selectRow(x[0].row())
        
    def order_add_one(self):
        x = self.order_table.selectedIndexes()
        if x:
            strs = self.order_table.model().data(x[0],Qt.DisplayRole)
            if len(self.seat.order_list) > x[0].row():
                self.seat.order_list[strs] += 1
                self.order_table_ui()
                self.order_table.selectRow(x[0].row())
            else :
                self.seat.free_list[strs] += 1
                self.order_table_ui()
                self.order_table.selectRow(x[0].row())
    
    def order_free_one(self):
        x = self.order_table.selectedIndexes()
        
        if x:
            strs = self.order_table.model().data(x[0],Qt.DisplayRole)
            self.seat.order_list[strs] -= 1
            
            if self.seat.order_list[strs] == 0:
                del self.seat.order_list[strs]
            else:
                self.order_table.selectRow(x[0].row())
            strs = strs + '(서비스)'
            if strs in self.seat.free_list:
                self.seat.free_list[strs] += 1
            else :
                self.seat.free_list[strs] = 1
            self.order_table_ui()

            
    def order_table_ui(self):
        column_headers = ['메뉴', '개당 가격', '개수', '총 가격']
        items = []
        for i in self.seat.order_list.keys():
            if self.seat.order_list[i] !=0 :
                items.append([i,18000,self.seat.order_list[i],self.seat.order_list[i]*18000])
                
        for i in self.seat.free_list.keys():
            if self.seat.free_list[i] !=0 :
                items.append([i,18000,self.seat.free_list[i],0])
                
        model = TableModel(pd.DataFrame(items, columns=column_headers))

        self.order_table.setModel(model)
        self.order_table.resizeColumnToContents(0)

        self.seat.value_setting()
        self.payment_print()
        self.parent.save()

    def payment_print(self):
        self.order_label.setText(str(self.seat.v_order))
        self.time_label.setText(str(self.seat.v_time))
        self.paid_label.setText(str(self.seat.payment.v_paid))
        self.discount_label.setText(str(self.seat.payment.v_discount))
        self.total_label.setText(str(self.seat.v_order + self.seat.v_time - self.seat.payment.v_discount - self.seat.payment.v_paid))

        self.order_label.show()
        self.time_label.show()
        self.paid_label.show()
        self.discount_label.show()
        self.total_label.show()
        
    def set_menu_text(self, init=False):
        for i in range(0,20):
            if self.page*20 + i >= len(self.menu_list):
                self.menu_buttons[i].setText('')
                self.menu_buttons[i].setDisabled(True)
            else:
                self.menu_buttons[i].setDisabled(False)
                self.menu_buttons[i].setText(self.menu_list[self.page*20+i]+'\n'+ str(self.value[self.page*20+i])+ '원')
        
    def menu_left(self):
        if self.page <=0:
            self.page = self.max_page
        else:
            self.page -=1
        self.set_menu_text()
            
    def menu_right(self):
        if self.page >= self.max_page:
            self.page = 0
        else:
            self.page +=1
        self.set_menu_text()

async def send_bot(massage): #실행시킬 함수명 임의지정
    api_key = ap.api_key
    channel_id = ap.channel_id
    bot = telegram.Bot(token = api_key)
    await bot.send_message(channel_id,massage)
