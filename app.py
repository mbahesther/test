from flask import Flask, request, render_template,redirect, flash, url_for
import os
import ssl
import smtplib
from email.message import EmailMessage
from threading import Thread
import re

from  jinja2 import FileSystemLoader, Environment

app = Flask(__name__)

app.config['SECRET_KEY'] = "123456"

SECRET_KEY='not_secure'
EMAIL_PASSWORD='ipaqitgjkllxbgtk'

environment = Environment(loader=FileSystemLoader("templates/"))   

@app.route('/', methods=['GET','POST'])
def index():
      return render_template('index.html')

#this route submit the form display in the register
@app.route('/form', methods=['GET','POST'])
def form():

    if request.method == "POST":
        fullname = request.form['fullname']
        email = request.form['email']
        msg = request.form['message']
        
  
        if not  fullname:
            flash("fullname can't empty")
            # redirect(url_for('contact'))

      
        if not  email:
            flash( "email can't be empty"),403
        email_pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if not re.match(email_pattern, email):
                        flash( "Invalid email input"),400

        if not msg: 
             flash( "Message can't be empty"),400

        message = f'Name :{fullname}\nMessage :{msg}\nEmail from :{email}'
        print(message)

        if fullname is not None and email is not None and msg is not None :
  
            
            email_receiver = 'omanovservices@gmail.com'
            email_password = EMAIL_PASSWORD
        
            subject = "New Email Alert"

            # body = (f''' You have received a new message from your website contact form. Here are details: {name},email:{email}, subject:{sub}, message:{msg} ''')
            em = EmailMessage()
            em['From'] = email
            em['To'] = email_receiver
            em['subject'] = subject
            em.set_content(message)

        

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_receiver, email_password)
                smtp.sendmail(email, email_receiver, em.as_string())

            flash("your form has been submitted")
            return redirect(url_for('contact')) 
    
        else:
            return 'test'
       
   


# @app.route('/index', methods=['GET'])
# def index():
     
              
#         # template = environment.get_template('index.html')
#         # return template.render() 
#         return render_template('index.html')


@app.route('/contact', methods=['GET'])
def contact():
     return render_template('contact.html', title="contact")   

# @app.route('/index', methods=['GET'])
# def index():
     
              
       
#         return render_template('index.html')



if __name__ == '__main__':

    app.run(host='0.0.0.0',debug=True, port=4000)