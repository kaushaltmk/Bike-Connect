from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import user_operation
from captcha.image import ImageCaptcha
import random
import hashlib
import stripe
from flask_mail import *
from admin import admin_operation
from bike import bike_operation

app = Flask(__name__)
app.secret_key = "ajkdas4a72bka89asd"  # object of Flask class
public_key = "pk_test_51NUv4eSFNAaaz8VZxcXi79TsJXwREjLkD6dCq9KIC4c9u2uzBNv2UygpXWj07fjlhkyTyIfbBj5DzpWm2Rl9CWkW00bb1jU1pw"
stripe.api_key = 'sk_test_51NUv4eSFNAaaz8VZ3Nzanb0ktn9wjL2D7i4Tkw7wlx1jOEabpk3FYWM4MjQDSJuGF1d36UIOpyfe95BjKe1K94gB00kfPWQszR'
# ---------------Mail configuration --------------------------------
app.config["MAIL_SERVER"] = 'smtp.office365.com'
app.config["MAIL_PORT"] = '587'
app.config["MAIL_USERNAME"] = 'yesiamkaushal@outlook.com'
app.config["MAIL_PASSWORD"] = 'IamKaushal7'
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)  # email object

# -------------------------------------------------------------------
@app.route("/")  # redirect to the first page of app
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/user_signup")
def user_signup():
    num = random.randrange(100000, 999999)
    # create an image instance of given size
    img = ImageCaptcha(width=280, height=90)
    global captcha_text  # Image captcha text
    captcha_text = str(num)  # convert captcha text into a string
    img.write(captcha_text, 'static/captcha/user_captcha.png')
    return render_template("user_signup.html")

@app.route("/user_signup_insert", methods=["GET", "POST"])
def user_signup_insert():
    if request.method == "POST":
        if (captcha_text != request.form['captcha']):
            flash("Invalid captcha!!!")
            return redirect(url_for("user_signup"))
        fname = request.form['fname']
        lname = request.form['lname']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        # -----------for profile photo upload------------
        photo = request.files['photo']
        photo_name = photo.filename
        photo.save("static/profile_photo/"+photo_name)
        # ----------password encryption----------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()
        ob = user_operation()  # object created of class from user module
        ob.user_signup_insert(fname, lname, mobile,email, password, photo_name)
        # -------------email verification-------------
        global otp
        otp = random.randint(100000, 999999)
        msg = Message('Email verification',sender='yesiamkaushal@outlook.com', recipients=[email])
        msg.body = "Hi " + fname + "\nPlease use the verification code below on the website \n\n Your email otp is : " + \
            str(otp) + "\n\n\n\nThanks!"
        mail.send(msg)
        flash("Successfully Registered !")
        return render_template('user_email_verify.html', email=email)

@app.route("/user_email_verify", methods=["GET", "POST"])
def user_email_verify():
    if request.method == "POST":
        user_otp = request.form['otp']
        if otp == int(user_otp):
            flash("Your mail is verified succesfully. You can Login Now!!!")
            return redirect(url_for('user_login'))
        email = request.form['email']
        op = user_operation()  # object created
        op.user_delete(email)
        flash("Your email verification is failed. Please try again with valid email")
        return redirect(url_for('user_signup'))

@app.route("/user_login")
def user_login():
    return render_template("user_login.html")

@app.route("/user_login_verify", methods=["GET", "POST"])
def user_login_verify():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        # ----------password encryption----------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()
        op = user_operation()  # object create
        r = op.user_login_verify(email, password)
        if (r == 0):
            flash("Invalid user email and password")
            return redirect(url_for('user_login'))
        else:
            return redirect(url_for('user_dashboard'))

@app.route("/user_logout")
def user_logout():
    session.clear()
    flash("Logged out successfully....login now!!")
    return redirect(url_for('user_login'))

@app.route("/user_dashboard")
def user_dashboard():
    if 'email' in session:
        op = user_operation()  # object create
        r = op.user_dashboard()
        return render_template("user_dashboard.html", record=r)
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('user_login'))

@app.route("/user_profile")
def user_profile():
    if "email" in session:
        op = user_operation()  # object create
        row = op.user_profile()
        return render_template("user_profile.html", record=row)
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('user_login'))

@app.route("/user_profile_update", methods=["GET", "POST"])
def user_profile_update():
    if "email" in session:
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            mobile = request.form['mobile']
            ob = user_operation()  # object
            ob.user_profile_update(fname, lname, mobile)
            flash("Your Profile updated successfully!!!")
            return redirect(url_for('user_profile'))
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('user_login'))

@app.route("/user_password_form")
def user_password_form():
    if "email" in session:
        return render_template("user_password_form.html")
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('user_login'))

@app.route("/user_password_change", methods=['POST', 'GET'])
def user_password_change():
    if "email" in session:
        if request.method == 'POST':
            oldpassword = request.form['oldpassword']
            newpassword = request.form['newpassword']
            # --- password encryption----------------#
            pas = hashlib.md5(oldpassword.encode())
            oldpassword = pas.hexdigest()
            pas = hashlib.md5(newpassword.encode())
            newpassword = pas.hexdigest()
            op = user_operation()  # object create
            r = op.user_password_change(oldpassword, newpassword)
            if (r == 0):
                flash("Your old password is invalid!!")
                return redirect(url_for('user_password_form'))
            else:
                session.clear()
                flash("Your password is updated successfully..login now!!")
                return redirect(url_for('user_login'))
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))

# ------------------------------------------------
# ----------------Admin Module ---------------------
# ------------------------------------------------

@app.route("/admin_signup")
def admin_signup():
    return render_template("admin_signup.html")

@app.route("/admin_signup_insert", methods=["GET", "POST"])
def admin_signup_insert():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        # --- password encryption----------------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()
        ob = admin_operation()  # object
        record = ob.admin_signup_insert(name, email, mobile, password)
        for r in record:
            flash("Your Admin ID : "+str(r[0]))
        return redirect(url_for('admin_login'))

@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")

@app.route("/admin_login_verify", methods=["GET", "POST"])
def admin_login_verify():
    # render_template("admin_login.html")
    if request.method == "POST":
        admin_id = request.form['admin_id']
        password = request.form['password']
        # ----------password encryption----------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()
        op = admin_operation()  # object create
        r = op.admin_login_verify(admin_id, password)
        if (r == 0):
            flash("Invalid admin_id and password")
            return redirect(url_for('admin_login'))
        else:
            return redirect(url_for('admin_dashboard'))

@app.route("/admin_dashboard")
def admin_dashboard():
    if 'email' in session:
        op = admin_operation()  # object create
        r = op.admin_dashboard()
        return render_template("admin_dashboard.html", record=r)
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('admin_login'))

@app.route("/admin_profile")
def admin_profile():
    if "email" in session:
        op = admin_operation()  # object create
        r1 = op.admin_profile()
        return render_template("admin_profile.html", rec=r1)
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('admin_login'))

@app.route("/admin_logout")
def admin_logout():
    session.clear()
    flash("Logged out successfully....login now!!")
    return redirect(url_for('admin_login'))

# -----------------CHANGE AND PASSWORD CHANGE---------------------#

@app.route("/admin_profile_update", methods=["GET", "POST"])
def admin_profile_update():
    if "email" in session:
        if request.method == "POST":
            name = request.form['name']
            mobile = request.form['mobile']
            ob = admin_operation()  # object
            ob.admin_profile_update(name, mobile)
            flash("Your Profile updated successfully!!!")
            return redirect(url_for('admin_profile'))
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('admin_login'))

@app.route("/admin_password_form")
def admin_password_form():
    if "email" in session:
        return render_template("admin_password_form.html")
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('admin_login'))

@app.route("/admin_password_change", methods=['POST', 'GET'])
def admin_password_change():
    if "email" in session:
        if request.method == 'POST':
            oldpassword = request.form['oldpassword']
            newpassword = request.form['newpassword']
            # --- password encryption----------------#
            pas = hashlib.md5(oldpassword.encode())
            oldpassword = pas.hexdigest()
            pas = hashlib.md5(newpassword.encode())
            newpassword = pas.hexdigest()
            op = admin_operation()  # object create
            r = op.admin_password_change(oldpassword, newpassword)
            if (r == 0):
                flash("Your old password is invalid!!")
                return redirect(url_for('admin_password_form'))
            else:
                session.clear()
                flash("Your password is updated successfully..login now!!")
                return redirect(url_for('admin_login'))
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('admin_login'))

# ----------------Bike Module--------------

@app.route("/addbike")
def addbike():
    return render_template("addbike.html")

@app.route("/add_bike")
def add_bike():
    if "admin_id" in session:
        return render_template("addbike.html")
    else:
        flash("You are not authorized ")
    return redirect(url_for('admin_login'))

@app.route("/add_bike_insert", methods=["GET", "POST"])
def add_bike_insert():
    if "admin_id" in session:
        if request.method == "POST":
            name = request.form['name']
            model = request.form['model']
            brand = request.form['brand']
            price = request.form['price']
            descrip = request.form['descrip']
        # -----------for bike photo upload------------
            photo = request.files['photo']
            photo_name = photo.filename
            photo.save("static/bike/"+photo_name)
            location = request.form['location']
            ob = bike_operation()  # object
            ob.add_bike(name, model, brand, price,
                        descrip, photo_name, location)
            flash("New bike is added successfully ",)
            return redirect(url_for('add_bike'))
    else:
        flash("You are not authorized")
        return redirect(url_for('admin_login'))

@app.route('/view_bikes')
def view_bikes():
    if "admin_id" in session:
        op = bike_operation()
        row = op.view_bikes()
        return render_template("view_bikes.html", record=row)
    else:
        flash("You are not authorized....Login Now!!!")
        return redirect(url_for('admin_login'))

@app.route('/view_bookings')
def view_bookings():
    if "admin_id" in session:
        op = admin_operation()
        row = op.view_bookings()
        return render_template("view_bookings.html", record=row)
    else:
        flash("You are not authorized....Login Now!!!")
        return redirect(url_for('admin_login'))

@app.route('/addbike_edit_form', methods=['POST', 'GET'])
def addbike_edit_form():
    if "admin_id" in session:
        if request.method == "GET":
            bikeid = request.args.get('bikeid')
            op = bike_operation()
            row = op.addbike_edit_form(bikeid)
            return render_template("addbike_edit_form.html", record=row)
    else:
        flash("You are not authorized....Login Now!!!")
        return redirect(url_for('admin_login'))

@app.route("/addbike_edit", methods=["GET", "POST"])
def addbike_edit():
    if "admin_id" in session:
        if request.method == "POST":
            bikeid = request.args.get('bikeid')
            model = request.form['model']
            price = request.form['price']
            descrip = request.form['descrip']
            location = request.form['location']
            ob = bike_operation()  # object
            ob.addbike_edit(model, price, descrip, location, bikeid)
            flash("Your data is updated successfully!!!"+str(bikeid))
            return redirect(url_for('view_bikes'))
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('admin_login'))

@app.route("/bike_delete", methods=["GET", "POST"])
def bike_delete():
    if "admin_id" in session:
        if request.method == "GET":
            test_id = request.args.get('bikeid')
            op = bike_operation()  # object create
            op.bike_delete(test_id)
            flash("Bike is deleted successfully!!")
            return redirect(url_for('view_bikes'))
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('admin_login'))

@app.route("/search_bike_form")
def bike_search_form():
    if "email" in session:
        return render_template("search_bike_form.html")
    else:
        flash("Log in to Continue.....!")
        return redirect(url_for('user_login'))

@app.route("/bike_search", methods=["GET", "POST"])
def bike_search():
    if "email" in session:
        if request.method == "POST":
            location = request.form['location']
            ob = user_operation()
            r = ob.bike_search(location)
            return render_template("search_bike_form.html", record=r, location=location)
        else:
            flash("You are not authorized...Login now!")
            return redirect(url_for('user_login'))

@app.route('/bike_book_request', methods=["GET", "POST"])
def bike_book_request():
    if "email" in session:
        ob = user_operation()
        r = ob.book_request()
        return render_template('bike_book_request.html', record=r)
    else:
        flash("You are not authorized...Login now!")
        return redirect(url_for('user_login'))

@app.route("/user_booking", methods=["GET", "POST"])
def user_booking():
    if "email" in session:
        if request.method == "POST":
            phone = request.form['phone']
            date = request.form['date']
            time = request.form['time']
            aadhar = request.form['aadhar']
            location = request.form['location']
            ob = user_operation()  # object
            row = ob.user_booking(phone, date, time, aadhar, location)
            return redirect(url_for('payment_success'))
    else:
        flash("You are not authorised.... login now!!")
        return redirect(url_for('user_login'))

@app.route("/payment_success", methods=["POST", "GET"])
def payment_success():
    if "email" in session:
        ob = user_operation()
        r = ob.payment_success()
        return render_template('payment_success.html', record=r)
    else:
        flash("You are not authorized...Login now!")
        return redirect(url_for('user_login'))

if __name__ == "__main__":
    app.run(debug=True)  # server activate
