from flask import render_template, request, flash, redirect, url_for, current_app
from . import contact
from .. import limiter
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio

@contact.route('/', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
async def contact_form():
    if request.method == 'POST':
        return await send_message()
    return render_template('contact.html', title='Contact CountryHopper')

async def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    if not all([name, email, subject, message]):
        flash('Please fill in all fields', 'error')
        return redirect(url_for('contact.contact_form'))
    
    try:
        msg = MIMEMultipart()
        msg['From'] = current_app.config['MAIL_USERNAME']
        msg['To'] = current_app.config['MAIL_USERNAME']
        msg['Subject'] = f"Contact Form: {subject}"
        
        body = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message: {message}
        """
        msg.attach(MIMEText(body, 'plain'))
        
        await aiosmtplib.send(
            msg,
            hostname=current_app.config['MAIL_SERVER'],
            port=current_app.config['MAIL_PORT'],
            use_tls=current_app.config['MAIL_USE_TLS'],
            username=current_app.config['MAIL_USERNAME'],
            password=current_app.config['MAIL_PASSWORD']
        )
        
        flash('Your message has been sent successfully!', 'success')
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        flash('Failed to send message. Please try again later.', 'error')
    
    return redirect(url_for('contact.contact_form'))
