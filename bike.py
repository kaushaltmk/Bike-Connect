import mysql.connector
from flask import session
    
class bike_operation:
    def connection(self):
        db=mysql.connector.connect(host="localhost", port="3306", user="root", password="root",database="project")
        return db
    
    def add_bike(self,name,model,brand,price,descrip,photo_name,location):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into bike (name,model,brand,price,descrip,photo,location) values(%s,%s,%s,%s,%s,%s,%s)"
        record=[name,model,brand,price,descrip,photo_name,location]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def view_bikes(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select * from bike"
        mycursor.execute(sq)
        row = mycursor.fetchall()
        db.commit()
        mycursor.close()
        db.close()
        return row
    
    def addbike_edit_form(self,bikeid):
        db=self.connection()
        mycursor=db.cursor()
        sq="select model,price,descrip,bikeid from bike where bikeid = %s "
        record=[bikeid]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def addbike_edit(self,model,price,descrip,location,bikeid):
        db=self.connection()
        mycursor=db.cursor()
        sq="update bike set model=%s, price=%s, descrip=%s,location=%s where bikeid=%s"
        record=[model,price,descrip,location,bikeid]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return 
    
    def bike_delete(self,admin_id):
        db = self.connection()
        mycursor = db.cursor()
        sq ="delete from bike where bikeid=%s"
        record=[admin_id]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
