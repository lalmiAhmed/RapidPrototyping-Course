import mysql.connector
from datetime import datetime

class Data_base():
    def __init__(self):
        self.db_name = 'sensor_readings'
        self.tb_name = 'humidity_and_temperature'

        self.mydb = mysql.connector.connect(
            host= 'localhost',
            user= 'zoro',
            password= 'okey',
            auth_plugin='mysql_native_password'
        )
        self.mycursor = self.mydb.cursor()
        # Create a DB if not exitsts
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self.db_name))
        self.mycursor.execute("USE {}".format(self.db_name))
        # Create a Table if not exitsts
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS {} (id int NOT NULL AUTO_INCREMENT, Humidity double(255,4), Temperature double(255,4), Time varchar(100),PRIMARY KEY(id))".format(self.tb_name))

    def store(self, records):
        values = ','.join("{}".format(e) for e in records)
        time = datetime.now().time().strftime('%H:%M:%S')
        values = values + ', "' +str(time) + '"'
        insert_formula ="INSERT INTO {} (Humidity, Temperature, Time) VALUES ({})".format(self.tb_name,values)
        self.mycursor.execute(insert_formula)                                        
        self.mydb.commit()     

    def show_columns(self):                                       
        self.mycursor.execute("show columns from {}".format(self.tb_name))                    
        return [c for c in self.mycursor]                                                
                                                                                  
    def fetch_column_values(self, col):                           
        show_col = "select {} from {}".format(col, self.tb_name)                         
        self.mycursor.execute(show_col)                                                  
        return [t for v in self.mycursor for t in v]   


