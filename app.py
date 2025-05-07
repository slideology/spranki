from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import json
import logging

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-goes-here')

# Set up logging
app.logger.setLevel(logging.ERROR)

def load_faq_data():
    faq_path = os.path.join(app.static_folder, 'data', 'faq.json')
    try:
        with open(faq_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        app.logger.error(f"FAQ data file not found at {faq_path}")
        return {}
    except json.JSONDecodeError as e:
        app.logger.error(f"Error decoding FAQ JSON: {str(e)}")
        return {}
    except Exception as e:
        app.logger.error(f"Unexpected error loading FAQ data: {str(e)}")
        return {}

def get_faqs_for_page(page_id):
    try:
        faq_data = load_faq_data()
        if page_id in faq_data:
            return {page_id: faq_data[page_id]}
        return {}
    except Exception as e:
        app.logger.error(f"Error getting FAQs for page {page_id}: {str(e)}")
        return {}

# Routes
@app.route('/')
def home():
    try:
        faq_data = get_faqs_for_page('index')
        return render_template('index.html', title='Spranki - Interactive Music Experience', faq_data=faq_data)
    except Exception as e:
        app.logger.error(f"Error in home route: {str(e)}")
        return render_template('index.html', title='Spranki - Interactive Music Experience', faq_data={})

@app.route('/about')
def about():
    return render_template('about.html', title='About Spranki')

@app.route('/game')
def game():
    return render_template('game.html', title='Play CountryHopper')

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/introduction')
def introduction():
    return render_template('introduction.html', title='Game Guide - Spranki')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return send_message()
    return render_template('contact.html', title='Contact CountryHopper')

@app.route('/faq')
def faq():
    try:
        faq_data = load_faq_data()
        return render_template('faq.html', title='FAQ - Spranki', faq_data=faq_data)
    except Exception as e:
        app.logger.error(f"Error in faq route: {str(e)}")
        return render_template('faq.html', title='FAQ - Spranki', faq_data={"faq_sections": []})

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/sprunki-misfismix')
def sprunki_misfismix():
    faq_data = get_faqs_for_page('sprunki-misfismix')
    return render_template('sprunki-misfismix.html',
                         page_title='Sprunki Misfismix',
                         faq_data=faq_data)

@app.route('/sprunki-pyramixed')
def sprunki_pyramixed():
    faq_data = get_faqs_for_page('sprunki-pyramixed')
    return render_template('sprunki-pyramixed.html',
                         page_title='Sprunki Pyramixed',
                         faq_data=faq_data)

@app.route('/sprunki-sprunksters')
def sprunki_sprunksters():
    faq_data = get_faqs_for_page('sprunki-sprunksters')
    return render_template('sprunki-sprunksters.html',
                         page_title='Sprunki Sprunksters',
                         faq_data=faq_data)

@app.route('/sprunki-sprured')
def sprunki_sprured():
    faq_data = get_faqs_for_page('sprunki-sprured')
    return render_template('sprunki-sprured.html',
                         page_title='Sprunki Sprured',
                         faq_data=faq_data)

@app.route('/sprunki-lily')
def sprunki_lily():
    faq_data = get_faqs_for_page('sprunki-lily')
    return render_template('sprunki-lily.html',
                         page_title='Sprunki Lily',
                         faq_data=faq_data)

@app.route('/sprunki-1996')
def sprunki_1996():
    """Sprunki 1996游戏页面路由"""
    faq_data = get_faqs_for_page('sprunki-1996')
    return render_template('sprunki-1996.html',
                          page_title='Sprunki 1996',
                          dynamic_faqs=faq_data['faqs'],
                          conclusion=faq_data['conclusion'])

@app.route('/sprunki-shatter')
def sprunki_shatter():
    faq_data = get_faqs_for_page('sprunki-shatter')
    return render_template('sprunki-shatter.html',
                         page_title='Sprunki Shatter',
                         faq_data=faq_data)

@app.route('/sprunki-fiddlebops')
def sprunki_fiddlebops():
    faq_data = get_faqs_for_page('sprunki-fiddlebops')
    return render_template('sprunki-fiddlebops.html',
                         page_title='Sprunki FiddleBops',
                         faq_data=faq_data)

@app.route('/incredibox-rainbow-animal')
def incredibox_rainbow_animal():
    faq_data = get_faqs_for_page('incredibox-rainbow-animal')
    return render_template('incredibox-rainbow-animal.html',
                         page_title='Incredibox Rainbow Animal',
                         faq_data=faq_data)

@app.route('/yet-another-boring-old-sprunki-mod')
def yet_another_boring_old_sprunki_mod():
    faq_data = get_faqs_for_page('yet-another-boring-old-sprunki-mod')
    return render_template('yet-another-boring-old-sprunki-mod.html',
                         page_title='Yet Another Boring Old Sprunki Mod',
                         faq_data=faq_data)

@app.route('/sprunki-wenda-edition')
def sprunki_wenda_edition():
    faq_data = get_faqs_for_page('sprunki-wenda-edition')
    return render_template('sprunki-wenda-edition.html',
                         page_title='Sprunki Wenda Edition',
                         faq_data=faq_data)

@app.route('/sprunki-pyramixed-ultimate-deluxe')
def sprunki_pyramixed_ultimate_deluxe():
    faq_data = get_faqs_for_page('sprunki-pyramixed-ultimate-deluxe')
    return render_template('sprunki-pyramixed-ultimate-deluxe.html',
                         page_title='Sprunki Pyramixed Ultimate Deluxe',
                         faq_data=faq_data)

@app.route('/sprunki-chaotic-good')
def sprunki_chaotic_good():
    faq_data = get_faqs_for_page('sprunki-chaotic-good')
    return render_template('sprunki-chaotic-good.html',
                         page_title='Sprunki Chaotic Good',
                         faq_data=faq_data)

@app.route('/incredibox-irrelevant-reunion')
def incredibox_irrelevant_reunion():
    faq_data = get_faqs_for_page('incredibox-irrelevant-reunion')
    return render_template('incredibox-irrelevant-reunion.html',
                         page_title='Incredibox Irrelevant Reunion',
                         faq_data=faq_data)

@app.route('/sprunki-pyramixed-melophobia')
def sprunki_pyramixed_melophobia():
    faq_data = get_faqs_for_page('sprunki-pyramixed-melophobia')
    return render_template('sprunki-pyramixed-melophobia.html',
                         page_title='Sprunki Pyramixed Melophobia',
                         faq_data=faq_data)

@app.route('/sprunka')
def sprunka():
    faq_data = get_faqs_for_page('sprunka')
    return render_template('sprunka.html',
                         page_title='Sprunka',
                         faq_data=faq_data)

@app.route('/sprunki-phase-6-definitive-all-alive')
def sprunki_phase_6_definitive_all_alive():
    faq_data = get_faqs_for_page('sprunki-phase-6-definitive-all-alive')
    return render_template('sprunki-phase-6-definitive-all-alive.html',
                         page_title='Sprunki Phase 6 Definitive All Alive',
                         faq_data=faq_data)

@app.route('/sprunki-phase-6-definitive-remaster')
def sprunki_phase_6_definitive_remaster():
    faq_data = get_faqs_for_page('sprunki-phase-6-definitive-remaster')
    return render_template('sprunki-phase-6-definitive-remaster.html',
                         page_title='Sprunki Phase 6 Definitive Remaster',
                         faq_data=faq_data)

@app.route('/sprunki-idle-clicker')
def sprunki_idle_clicker():
    faq_data = get_faqs_for_page('sprunki-idle-clicker')
    return render_template('sprunki-idle-clicker.html',
                         page_title='Sprunki Idle Clicker',
                         faq_data=faq_data)

@app.route('/sprunki-phase-6-definitive')
def sprunki_phase_6_definitive():
    faq_data = get_faqs_for_page('sprunki-phase-6-definitive')
    return render_template('sprunki-phase-6-definitive.html',
                         page_title='Sprunki Phase 6 Definitive',
                         faq_data=faq_data)

@app.route('/sprunki-sploinkers')
def sprunki_sploinkers():
    faq_data = get_faqs_for_page('sprunki-sploinkers')
    return render_template('sprunki-sploinkers.html',
                         page_title='Sprunki Sploinkers',
                         faq_data=faq_data)

@app.route('/sprunki-pyramixed-regretful')
def sprunki_pyramixed_regretful():
    faq_data = get_faqs_for_page('sprunki-pyramixed-regretful')
    return render_template('sprunki-pyramixed-regretful.html',
                         page_title='Sprunki Pyramixed Regretful',
                         faq_data=faq_data)

@app.route('/sprunki-megalovania')
def sprunki_megalovania():
    faq_data = get_faqs_for_page('sprunki-megalovania')
    return render_template('sprunki-megalovania.html',
                         page_title='Sprunki Megalovania',
                         faq_data=faq_data)

@app.route('/sprunki-sprunkr')
def sprunki_sprunkr():
    faq_data = get_faqs_for_page('sprunki-sprunkr')
    return render_template('sprunki-sprunkr.html',
                         page_title='Sprunkr',
                         faq_data=faq_data)

@app.route('/sprunki-brud-edition-finale')
def sprunki_brud_edition_finale():
    faq_data = get_faqs_for_page('sprunki-brud-edition-finale')
    return render_template('sprunki-brud-edition-finale.html',
                         page_title='Sprunki Brud Edition Finale',
                         faq_data=faq_data)

@app.route('/sprunki-spruted')
def sprunki_spruted():
    faq_data = get_faqs_for_page('sprunki-spruted')
    return render_template('sprunki-spruted.html',
                         page_title='Sprunki Spruted',
                         faq_data=faq_data)

@app.route('/sprunki-spfundi')
def sprunki_spfundi():
    faq_data = get_faqs_for_page('sprunki-spfundi')
    return render_template('sprunki-spfundi.html',
                         page_title='Sprunki Spfundi',
                         faq_data=faq_data)

@app.route('/internet-roadtrip')
def internet_roadtrip():
    try:
        app.logger.info("Accessing internet-roadtrip route")
        faq_data = get_faqs_for_page('internet-roadtrip')
        return render_template('internet-roadtrip.html',
                            page_title='Internet Roadtrip',
                            faq_data=faq_data)
    except Exception as e:
        app.logger.error(f"Error in internet-roadtrip route: {str(e)}")
        return render_template('error.html', error_message="An error occurred while loading the page"), 500

@app.route('/sprunki-angry')
def sprunki_angry():
    faq_data = get_faqs_for_page('sprunki-angry')
    return render_template('sprunki-angry.html',
                         page_title='Sprunki Angry',
                         faq_data=faq_data)

@app.route('/sprunki-phase-777-3-7')
def sprunki_phase_777_3_7():
    faq_data = get_faqs_for_page('sprunki-phase-777-3-7')
    return render_template('sprunki-phase-777-3-7.html',
                         page_title='Sprunki Phase 777 3.7',
                         faq_data=faq_data)

@app.route('/sprunklings')
def sprunklings():
    faq_data = get_faqs_for_page('sprunki-sprunklings')
    return render_template('sprunklings.html',
                         page_title='Sprunklings',
                         faq_data=faq_data)

@app.route('/sprunki-swap-retextured')
def sprunki_swap_retextured():
    faq_data = get_faqs_for_page('sprunki-swap-retextured')
    return render_template('sprunki-swap-retextured.html',
                         page_title='Sprunki Swap Retextured',
                         faq_data=faq_data)

@app.route('/sprunki-upin-ipin')
def sprunki_upin_ipin():
    faq_data = get_faqs_for_page('sprunki-upin-ipin')
    return render_template('sprunki-upin-ipin.html',
                         page_title='Sprunki Upin Ipin',
                         faq_data=faq_data)

@app.route('/sprunki-ultimate-deluxe')
def sprunki_ultimate_deluxe():
    faq_data = get_faqs_for_page('sprunki-ultimate-deluxe')
    return render_template('sprunki-ultimate-deluxe.html',
                         page_title='Sprunki Ultimate Deluxe',
                         faq_data=faq_data)

@app.route('/sprunki-phase-19-update')
def sprunki_phase_19_update():
    faq_data = get_faqs_for_page('sprunki-phase-19-update')
    return render_template('sprunki-phase-19-update.html',
                         page_title='Sprunki Phase 19 Update',
                         faq_data=faq_data)

@app.route('/sprunki-phase-1-7')
def sprunki_phase_1_7():
    faq_data = get_faqs_for_page('sprunki-phase-1-7')
    return render_template('sprunki-phase-1-7.html',
                         page_title='Sprunki Phase 1.7',
                         faq_data=faq_data)

@app.route('/sprunki-dx')
def sprunki_dx():
    faq_data = get_faqs_for_page('sprunki-dx')
    return render_template('sprunki-dx.html',
                         page_title='Sprunki DX',
                         faq_data=faq_data)

@app.route('/sprunki-banana')
def sprunki_banana():
    faq_data = get_faqs_for_page('sprunki-banana')
    return render_template('sprunki-banana.html',
                         page_title='Sprunki Banana',
                         faq_data=faq_data)

@app.route('/sprunki-garnold')
def sprunki_garnold():
    faq_data = get_faqs_for_page('sprunki-garnold')
    return render_template('sprunki-garnold.html',
                         page_title='Sprunki Garnold',
                         faq_data=faq_data)

@app.route('/sprunki-ketchup')
def sprunki_ketchup():
    faq_data = get_faqs_for_page('sprunki-ketchup')
    return render_template('sprunki-ketchup.html',
                         page_title='Sprunki Ketchup',
                         faq_data=faq_data)

@app.route('/sprunki-agents')
def sprunki_agents():
    faq_data = get_faqs_for_page('sprunki-agents')
    return render_template('sprunki-agents.html',
                         page_title='Sprunki Agents',
                         faq_data=faq_data)

@app.route('/sprunki-banana-porridge')
def sprunki_banana_porridge():
    faq_data = get_faqs_for_page('sprunki-banana-porridge')
    return render_template('sprunki-banana-porridge.html',
                         page_title='Sprunki Banana Porridge',
                         faq_data=faq_data)

@app.route('/sprunki-retake-but-human')
def sprunki_retake_but_human():
    faq_data = get_faqs_for_page('sprunki-retake-but-human')
    return render_template('sprunki-retake-but-human.html',
                         page_title='Sprunki Retake But Human',
                         faq_data=faq_data)

@app.route('/sprunki-retake-new-human')
def sprunki_retake_new_human():
    faq_data = get_faqs_for_page('sprunki-retake-new-human')
    return render_template('sprunki-retake-new-human.html',
                         page_title='Sprunki Retake New Human',
                         faq_data=faq_data)

@app.route('/sprunki-grown-up')
def sprunki_grown_up():
    faq_data = get_faqs_for_page('sprunki-grown-up')
    return render_template('sprunki-grown-up.html',
                         page_title='Sprunki Grown Up',
                         faq_data=faq_data)

@app.route('/sprunki-parodybox')
def sprunki_parodybox():
    faq_data = get_faqs_for_page('sprunki-parodybox')
    return render_template('sprunki-parodybox.html',
                         page_title='Sprunki Parodybox',
                         faq_data=faq_data)

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

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
        app.logger.error(f"Error sending message: {str(e)}")
        flash('Sorry, there was a problem sending your message. Please try again later.', 'error')
    
    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True, port=5006)
