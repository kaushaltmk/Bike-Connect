import mysql.connector
from flask import session
    
class admin_operation:
    def connection(self):
        db=mysql.connector.connect(host="localhost", port="3306", user="root", password="root",database="project")
        return db
    
    def admin_signup_insert(self,name,email,mobile,password):
        db = self.connection()
        mycursor = db.cursor()
        sq ="insert into admin (name,email,mobile,password) values(%s,%s,%s,%s)"
        record=[name,email,mobile,password]
        mycursor.execute(sq,record)
        db.commit()
        sq ="select admin_id from admin order by admin_id desc limit 1"
        mycursor.execute(sq)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
    
    def admin_login_verify(self,admin_id,password):
        db=self.connection()
        mycursor=db.cursor()
        sq="select email,name,admin_id from admin where admin_id=%s and password=%s"
        record=[admin_id,password]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        r=mycursor.rowcount
        mycursor.close()
        db.close()
        if(r==0):
            return 0
        else:
            for rec in row:
                session['email']=rec[0]
                session['name']=rec[1]
                session['admin_id']=rec[2]
            return 1
        
    def admin_profile(self):
        db = self.connection()
        mycursor = db.cursor()
        sq ="select name,email,mobile,password from admin where email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def admin_dashboard(self):
        db = self.connection()
        mycursor = db.cursor()
        sq ="select * from booking order by booking_id desc limit 3"
        mycursor.execute(sq)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def view_bookings(self):
        db = self.connection()
        mycursor = db.cursor()
        sq ="select * from booking "
        mycursor.execute(sq)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def admin_profile_update(self,name,mobile):
        db = self.connection()
        mycursor = db.cursor()
        sq ="update admin set name=%s,mobile=%s where email=%s"
        record=[name,mobile,session['email']]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return
    
    def admin_password_change(self, oldpassword, newpassword):
        db = self.connection()
        mycursor = db.cursor()
        sq = "SELECT password FROM admin WHERE password=%s and  email = %s"
        record = [oldpassword,session['email']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        r=mycursor.rowcount
        if (r==0):
            # No user found with the given email
            return 0
        else:
            # Update the password
            sq = "UPDATE admin SET password = %s WHERE email = %s"
            record = [newpassword, session['email']]
            mycursor.execute(sq, record)
            db.commit()
            mycursor.close()
            db.close()
            return 1
    