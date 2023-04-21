
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from datetime import datetime
import pandas as pd

payment_ui = uic.loadUiType('payment.ui')[0]

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

#payment_ui
class Payment_Class(QDialog, payment_ui):
    def __init__(self, parent, payment_list = []):
        super( ).__init__()
        self.number_value = "0"
        self.v_discount = 0
        self.v_paid = 0
        self.payment_list = payment_list
        self.result = False
        self.parent = parent

        self.initUI()
        #self.show()

    def initUI(self):
        self.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)

        #number
        self.number0.clicked.connect(lambda : self.clicked_number('0'))
        self.number1.clicked.connect(lambda : self.clicked_number('1'))
        self.number2.clicked.connect(lambda : self.clicked_number('2'))
        self.number3.clicked.connect(lambda : self.clicked_number('3'))
        self.number4.clicked.connect(lambda : self.clicked_number('4'))
        self.number5.clicked.connect(lambda : self.clicked_number('5'))
        self.number6.clicked.connect(lambda : self.clicked_number('6'))
        self.number7.clicked.connect(lambda : self.clicked_number('7'))
        self.number8.clicked.connect(lambda : self.clicked_number('8'))
        self.number9.clicked.connect(lambda : self.clicked_number('9'))
        self.number00.clicked.connect(lambda : self.clicked_number('00'))
        self.number000.clicked.connect(lambda : self.clicked_number('000'))
        
        self.number_del.clicked.connect(lambda : self.clicked_del())
        self.number_clear.clicked.connect(lambda : self.clicked_clear())
        self.number_all.clicked.connect(lambda : self.clicked_all())

        self.Pay_cash.clicked.connect(lambda : self.clicked_payment('현금'))
        self.Pay_discount.clicked.connect(lambda : self.clicked_payment('할인'))
        self.Pay_credit.clicked.connect(lambda : self.clicked_payment('카드'))
        self.Pay_bank.clicked.connect(lambda : self.clicked_payment('계좌'))
        
        self.Pay_close.clicked.connect(self.clicked_close)
        self.Pay_all.clicked.connect(self.clicked_payall)
        self.Pay_all.setEnabled(False)

        self.Pay_table.setSelectionBehavior(QTableView.SelectRows)
        self.Pay_cancel.clicked.connect(self.clicked_cancel)

        self.payment_setting()
        self.payment_print()

    def reset(self):
        self.number_value = "0"
        self.v_discount = 0
        self.v_paid = 0
        self.payment_list = []
        self.result = False
        self.payment_print()
        
        self.Pay_all.setEnabled(False)
        self.Pay_all.show()

    def clicked_cancel(self):
        x = self.Pay_table.selectedIndexes()
        if x:
            strs = self.Pay_table.model().data(x[0],Qt.DisplayRole)
            if len(self.payment_list) > x[0].row():
                del self.payment_list[x[0].row()]
                self.payment_setting()
                self.payment_print()
            
    def payment_table_ui(self):
        column_headers = ['결제 시간', '결제 타입', '결제 금액']
        model = TableModel(pd.DataFrame(self.payment_list, columns=column_headers))

        self.Pay_table.setModel(model)
        self.Pay_table.resizeColumnToContents(0)

    def payment_setting(self):
        self.v_discount = 0
        self.v_paid = 0
        self.number_value = "0"
        for i in range(len(self.payment_list)):
            if self.payment_list[i][1] == '할인':
                self.v_discount += self.payment_list[i][2]
            elif self.payment_list[i][1] == '현금':
                self.v_paid += self.payment_list[i][2]
            elif self.payment_list[i][1] == '카드':
                self.v_paid += self.payment_list[i][2]
            elif self.payment_list[i][1] == '계좌':
                self.v_paid += self.payment_list[i][2]
        self.print()

    def payment_print(self):
        self.order_label.setText(str(self.parent.v_order))
        self.time_label.setText(str(self.parent.v_time))
        self.paid_label.setText(str(self.v_paid))
        self.discount_label.setText(str(self.v_discount))
        tmp = self.parent.v_order + self.parent.v_time - self.v_discount - self.v_paid
        self.total_label.setText(str(tmp))

        self.order_label.show()
        self.time_label.show()
        self.paid_label.show()
        self.discount_label.show()
        self.total_label.show()
        self.payment_table_ui()

        if tmp == 0 :
            self.Pay_all.setEnabled(True)
            self.Pay_all.show()
        else:
            self.Pay_all.setEnabled(False)
            self.Pay_all.show()
    
    def clicked_close(self):
        self.close()

    def clicked_payall(self):
        self.result = True
        self.Pay_all.setEnabled(False)
        self.Pay_all.show()
        self.close()

    def clicked_payment(self, option):
        if self.number_value == "0":
            return
        now = datetime.now()
        self.payment_list.append([now.strftime("%Y-%m-%d %H:%M:%S"),option,int(self.number_value)])
        self.number_value = "0"
        self.payment_setting()
        self.payment_print()

    def clicked_all(self):
        self.number_value = str(self.parent.v_order + self.parent.v_time - self.v_discount - self.v_paid)
        self.print()
    
    def clicked_clear(self):
        self.number_value = "0"
        self.print()

    def clicked_del(self):
        if len(self.number_value) == 1:
            self.number_value = '0'
        else:
            self.number_value = self.number_value[:-1]
        self.print()


    def clicked_number(self, strs):
        if self.number_value =='0' and (strs=='0' or strs=='00' or strs=='000'):
            self.number_value = self.number_value
        elif self.number_value == '0':
            self.number_value = strs
        else:
            self.number_value = self.number_value + strs
        self.print()


    def print(self):
        self.number_label.setText(self.number_value)
        self.number_label.show()

class double_Payment(Payment_Class):
    def __init__(self, parent, payment_list = []):
        super( ).__init__()
        self.number_value = "0"
        self.v_discount = 0
        self.v_paid = 0
        self.payment_list = payment_list
        self.result = False
        self.parent = parent

        self.initUI()