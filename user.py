import mysql.connector
from flask import session

class user_operation:
    def connection(self):
        db=mysql.connector.connect(host="localhost",port="3306",user="root",password="root",database="project")
        return db
    
    def user_signup_insert(self,fname,lname,email,mobile,password,photo_name):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into user(fname,lname,email,mobile,password,photo) values(%s,%s,%s,%s,%s,%s)"
        record=[fname,lname,mobile,email,password,photo_name]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def user_delete(self,email):
        db = self.connection()
        mycursor=db.cursor()
        sq = "delete from user where email=%s"
        record=[email]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def user_login_verify(self,email,password):
        db=self.connection()
        mycursor=db.cursor()
        sq="select fname,email from user where email=%s and password=%s"
        record=[email,password]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        r=mycursor.rowcount
        mycursor.close()
        db.close()
        if(r==0):
            return 0
        else:
            for rec in row:
                session['name']=rec[0]
                session['email']=rec[1]
            return 1

    def user_profile(self):
        db = self.connection()
        mycursor = db.cursor()
        sq ="select fname,lname,email,mobile from user where email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def user_dashboard(self):
        db = self.connection()
        mycursor = db.cursor()
        sq ="select * from booking order by booking_id desc limit 5"
        mycursor.execute(sq)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def book_request(self):
        db = self.connection()
        mycursor = db.cursor()
        sq ="select * from bike "
        mycursor.execute(sq)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def user_profile_update(self,fname,lname,mobile):
        db = self.connection()
        mycursor = db.cursor()
        sq ="update user set fname=%s,lname=%s,mobile=%s where email=%s"
        record=[fname,lname,mobile,session['email']]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def user_password_change(self, oldpassword, newpassword):
        db = self.connection()
        mycursor = db.cursor()
        sq = "SELECT password FROM user WHERE password=%s and  email = %s"
        record = [oldpassword,session['email']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        r=mycursor.rowcount
        if (r==0):
            # No user found with the given email
            return 0
        else:
            # Update the password
            sq = "UPDATE user SET password = %s WHERE email = %s"
            record = [newpassword, session['email']]
            mycursor.execute(sq, record)
            db.commit()
            mycursor.close()
            db.close()
            return 1
        
    def bike_search(self,location):
        db = self.connection()
        mycursor = db.cursor()
        sq= "select * from bike where location=%s "
        record=[location]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    
    def user_booking(self,phone,date,time,aadhar,location):
        db = self.connection()
        mycursor = db.cursor()
        sq ="insert into booking (email,phone,date,time,aadhar,location) values(%s,%s,%s,%s,%s,%s)"
        record=[session['email'],phone,date,time,aadhar,location]
        mycursor.execute(sq,record)
        db.commit()
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row 

    def payment_success(self):
        db = self.connection()
        mycursor = db.cursor()
        sq= "select * from booking order by booking_id desc limit 1"
        # sq= "select name,model,brand,price from bike  " 
        mycursor.execute(sq)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def book_request(self):
        db = self.connection()
        mycursor = db.cursor()
        sq= "select * from booking "
        record=[]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def user_book_history(self):
        db = self.connection()
        mycursor = db.cursor()
        sq="select book_id,type,charges,appoint_date from test t, book b where t.testid=b.testid and user_email=%s"
        record=[session['user_email']]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
