from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-goes-here')

# Routes
@app.route('/')
def home():
    return render_template('index.html', title='CountryHopper - Interactive Geography Game')

@app.route('/about')
def about():
    return render_template('about.html', title='About CountryHopper')

@app.route('/game')
def game():
    return render_template('game.html', title='Play CountryHopper')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return send_message()
    return render_template('contact.html', title='Contact CountryHopper')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    if not all([name, email, subject, message]):
        flash('Please fill in all fields', 'error')
        return redirect(url_for('contact'))
    
    try:
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        
        if not email_user or not email_password:
            flash('Email configuration is not set up', 'error')
            return redirect(url_for('contact'))
        
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_user  # Send to yourself
        msg['Subject'] = f"CountryHopper: {subject} - from {name}"
        
        body = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message: {message}
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)
        server.quit()
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
    except Exception as e:
        flash('Sorry, there was a problem sending your message. Please try again later.', 'error')
    
    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
