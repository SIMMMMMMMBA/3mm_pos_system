#%%
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from datetime import datetime
import pickle
import os
import pandas as pd
import math
import copy
import telegram
import api_key

import asyncio

# 더 추가할 필요가 있다면 추가하시면 됩니다. 예: (from PyQt5.QtGui import QIcon)
'''
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))    
    return os.path.join(base_path, relative_path)

form = resource_path('/Users/simba/3mm Pos system.ui')
'''
menu_ui = uic.loadUiType('menu.ui')[0]
desk_ui = uic.loadUiType('desk.ui')[0]
async def send_bot(massage): #실행시킬 함수명 임의지정
    api_key = api_key.api_key
    channel_id = api_key.channel_id
    bot = telegram.Bot(token = api_key)
    await bot.send_message(channel_id,massage)
    
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
    
class seat_button(QPushButton):
    def __init__(self, parent, name="", title="", total=0, start_time=0, order_list={}, free_list = {}, x=None, y=None):
        super().__init__(title, parent)
        self.name = name
        self.total = total
        self.start_time = start_time
        self.order_list = copy.deepcopy(order_list)
        self.free_list = copy.deepcopy(free_list)
        self.parent = parent
        if x:
            self.move(x,y)
            
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
        
    def printing(self):
        strings = self.name + "\n\n"
        tot = 0
        cnt = 0
        for i in self.order_list.keys():
            if cnt >=3 :
                pass
            elif self.order_list[i]!=0:
                strings = strings + i +' '+ str(self.order_list[i]) +"\n"
                cnt+=1
            tot += 18000 * self.order_list[i]
            
        strings = strings + "\n"
        if self.start_time == 0 and tot == 0:
            strings = strings + "빈 좌석\n"
        elif self.start_time == 0:
            strings = strings + "시간 시작 안함\n"
        else :
            strings = strings + self.start_time.strftime("%Y년 %m월 %d일 %H시 %M분") + "\n"
        
        strings = strings + '\n' + str(tot) + '원\n'
        

            
        self.setText(strings)
            
    def save(self):
        return {'name': self.name,
                'total': self.total,
                'start_time' : self.start_time,
                'order_list' : self.order_list,
                'free_list' : self.free_list,
                'x' : self.x(),
                'y' : self.y()}
      
'''
class order_list():
    def __init__(self):
        self.menu = 
'''

        
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
        
    def ending_time(self):
        self.start.setDisabled(False)
        end_time = datetime.now()
        self.end.setDisabled(True)
        asyncio.run(send_bot(self.seat.name + end_time.strftime(" %Y년 %m월 %d일 %H시 %M분 퇴실")))
        self.seat.start_time = 0
        

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
        
        #start 관련
        
        #결제 관련
        
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
        '''
        width = self.order_table.width()
        self.order_table.setColumnWidth(0, width*3)
        self.order_table.setColumnWidth(1, width*1)
        self.order_table.setColumnWidth(2, width*2)
        '''
        self.parent.save()
        
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
            self.menu = Menu_Class(seat, self)
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
        
if __name__ == '__main__':
    #asyncio.run(send_bot('Program booting')) #봇 실행하는 코드
    os.makedirs('data',exist_ok=True)
    app = QApplication(sys.argv)
    myWindow = Desk_Class()
    app.exec_()
    
    
#%%

