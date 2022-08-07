from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from psuedoSensor import PseudoSensor
#from database_f import Data_base
from datetime import datetime
from matplotlib import pyplot as plt


class Main_UI(qtw.QWidget):
    def __init__(self):
        super(Main_UI, self).__init__()
        #Load the UI file
        uic.loadUi('humidity_reader.ui', self)

        #Storage vars
        self.hum_list = []
        self.temp_list = []
        self.time_list = []

        #Define UI widgets
        self.read_btn = self.findChild(qtw.QPushButton, 'read_btn')
        self.read_many = self.findChild(qtw.QPushButton, 'pushButton')
        self.tmp_lcd = self.findChild(qtw.QLCDNumber, 'temp_out')
        self.hum_lcd = self.findChild(qtw.QLCDNumber, 'hum_out')
        self.table = self.findChild(qtw.QTableWidget, 'table')
        self.table_2 = self.findChild(qtw.QTableWidget, 'table_2')
        self.close_btn = self.findChild(qtw.QPushButton, 'close_btn')
        self.analyse_btn = self.findChild(qtw.QPushButton, 'analyse_btn')
        self.hum_alarm = self.findChild(qtw.QLineEdit, "hum_alarm")
        self.temp_alarm = self.findChild(qtw.QLineEdit, "temp_alarm")
        self.plot_btn = self.findChild(qtw.QPushButton, 'plot_btn')
        
        # Initialize my sensor reader 
        self.ps = PseudoSensor()

        #Initialize a timer
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.read_multi_values)

        #Action
        self.read_btn.clicked.connect(self.read_values)
        self.read_many.clicked.connect(self.start_reading)
        self.close_btn.clicked.connect(self.close)
        self.analyse_btn.clicked.connect(self.analyse_function)
        self.plot_btn.clicked.connect(self.plot)
        #Show 
        self.show()

    def read_values(self):
        hum, temp = self.ps.generate_values()
        # Display the readings
        self.tmp_lcd.display(temp)
        self.hum_lcd.display(hum)
        # Stor readings to the DB
        #my_DB = Data_base()
        #my_DB.store([hum, temp])
    
    def read_multi_values(self):
        # Add the readings to the table
        hum, temp = self.ps.generate_values()
        time = datetime.now().time().strftime('%H:%M:%S')
        # Setting Alarms
        if self.hum_alarm.text() != "":
            h_limit = float(self.hum_alarm.text())
        else:
            h_limit = 60
       
        if self.temp_alarm.text() != "":
            t_limit = float(self.temp_alarm.text())
        else:
            t_limit = 80
        if hum > h_limit:
            self.hum_alarm.setText(str(hum))
            self.hum_alarm.setStyleSheet("QLineEdit { background: yellow; color: red;}")
            self.hum_alarm.setAlignment(qtc.Qt.AlignCenter)
        if temp > t_limit:
            self.temp_alarm.setText(str(temp))
            self.temp_alarm.setStyleSheet("QLineEdit { background: yellow; color: red;}")
            self.temp_alarm.setAlignment(qtc.Qt.AlignCenter)
        
        self.time_list.append(time)
        self.hum_list.append(hum)
        self.temp_list.append(temp)
        row = self.table.rowCount()
        self.table.setRowCount(row+1)
        self.table.setColumnCount(3)
        self.table.setItem(row, 0, qtw.QTableWidgetItem(str(hum)))
        self.table.setItem(row, 1, qtw.QTableWidgetItem(str(temp)))
        self.table.setItem(row, 2, qtw.QTableWidgetItem(str(time)))
        # Stor readings to the DB
        #my_DB = Data_base()
        #my_DB.store([hum, temp])
        # Stop the timer for 10 readings
        if self.table.rowCount() >= 10:
            self.timer.stop()
            self.plot_btn.setEnabled(True)
    
    def start_reading(self):
        while (self.table.rowCount() > 0):
            self.table.removeRow(0)
            self.hum_list = []
            self.temp_list = []
        self.timer.start(1000)
    
    def analyse_function(self):
        if len(self.hum_list ) != 0 and len(self.temp_list) !=0:
            self.table_2.setItem(0, 0, qtw.QTableWidgetItem(str(max(self.hum_list))))
            self.table_2.setItem(1, 0, qtw.QTableWidgetItem(str(max(self.temp_list))))
            self.table_2.setItem(0, 1, qtw.QTableWidgetItem(str(min(self.hum_list))))
            self.table_2.setItem(1, 1, qtw.QTableWidgetItem(str(min(self.temp_list))))
            self.table_2.setItem(0, 2, qtw.QTableWidgetItem(str(round(sum(self.hum_list)/len(self.hum_list), 4))))
            self.table_2.setItem(1, 2, qtw.QTableWidgetItem(str(round(sum(self.temp_list)/len(self.temp_list), 4))))
    
    def plot(self):
        time_axis = self.time_list
        hum_axis = self.hum_list
        temp_axis = self.temp_list
        plt.plot(time_axis, hum_axis, 'g')
        plt.plot(time_axis, temp_axis, 'r')
        plt.legend(['Humidity','Temperature'])
        plt.ylabel('Humidity and Temperature')                                                          
        plt.xlabel('Time')                                                              
        plt.title("Humidity & Temperature Graph")                                                    
        plt.grid(True)                                                                
        plt.tight_layout()                                                              
        plt.show() 


if __name__ == '__main__': 
    app = qtw.QApplication([])
    ui = Main_UI()
    app.exec_()
