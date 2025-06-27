from flask import Flask, render_template, send_from_directory
import os
import json
import logging

app = Flask(__name__)

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

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Spranki')

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
    return render_template('game-template.html',
                         page_title='Sprunki Pyramixed',
                         page_slug='sprunki-pyramixed',
                         faq_data=faq_data)

@app.route('/sprunki-sprunksters')
def sprunki_sprunksters():
    faq_data = get_faqs_for_page('sprunki-sprunksters')
    return render_template('game-template.html',
                         page_title='Sprunki Sprunksters',
                         page_slug='sprunki-sprunksters',
                         faq_data=faq_data)

@app.route('/sprunki-sprured')
def sprunki_sprured():
    faq_data = get_faqs_for_page('sprunki-sprured')
    return render_template('game-template.html',
                         page_title='Sprunki Sprured',
                         page_slug='sprunki-sprured',
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
    # 提取正确的数据格式
    game_data = faq_data.get('sprunki-1996', {})
    return render_template('sprunki-lily.html',  # 暂时使用现有模板
                          page_title='Sprunki 1996', 
                          faq_data=faq_data)

@app.route('/sprunki-shatter')
def sprunki_shatter():
    faq_data = get_faqs_for_page('sprunki-shatter')
    return render_template('game-template.html',
                         page_title='Sprunki Shatter',
                         page_slug='sprunki-shatter',
                         faq_data=faq_data)

@app.route('/sprunki-fiddlebops')
def sprunki_fiddlebops():
    faq_data = get_faqs_for_page('sprunki-fiddlebops')
    return render_template('game-template.html',
                         page_title='Sprunki Fiddlebops',
                         page_slug='sprunki-fiddlebops',
                         faq_data=faq_data)

@app.route('/incredibox-rainbow-animal')
def incredibox_rainbow_animal():
    faq_data = get_faqs_for_page('incredibox-rainbow-animal')
    return render_template('game-template.html',
                         page_title='Sprunki Incredibox Rainbow Animal',
                         page_slug='incredibox-rainbow-animal',
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
    return render_template('game-template.html',
                         page_title='Sprunki Wenda Edition',
                         page_slug='sprunki-wenda-edition',
                         faq_data=faq_data)

@app.route('/sprunki-pyramixed-ultimate-deluxe')
def sprunki_pyramixed_ultimate_deluxe():
    faq_data = get_faqs_for_page('sprunki-pyramixed-ultimate-deluxe')
    return render_template('game-template.html',
                         page_title='Sprunki Pyramixed Ultimate Deluxe',
                         page_slug='sprunki-pyramixed-ultimate-deluxe',
                         faq_data=faq_data)

@app.route('/sprunki-chaotic-good')
def sprunki_chaotic_good():
    faq_data = get_faqs_for_page('sprunki-chaotic-good')
    return render_template('game-template.html',
                         page_title='Sprunki Chaotic Good',
                         page_slug='sprunki-chaotic-good',
                         faq_data=faq_data)

@app.route('/incredibox-irrelevant-reunion')
def incredibox_irrelevant_reunion():
    faq_data = get_faqs_for_page('incredibox-irrelevant-reunion')
    return render_template('game-template.html',
                         page_title='Sprunki Incredibox Irrelevant Reunion',
                         page_slug='incredibox-irrelevant-reunion',
                         faq_data=faq_data)

@app.route('/sprunki-pyramixed-melophobia')
def sprunki_pyramixed_melophobia():
    faq_data = get_faqs_for_page('sprunki-pyramixed-melophobia')
    return render_template('game-template.html',
                         page_title='Sprunki Pyramixed Melophobia',
                         page_slug='sprunki-pyramixed-melophobia',
                         faq_data=faq_data)

@app.route('/sprunka')
def sprunka():
    faq_data = get_faqs_for_page('sprunka')
    return render_template('game-template.html',
                         page_title='Sprunki Sprunka',
                         page_slug='sprunka',
                         faq_data=faq_data)

@app.route('/sprunki-phase-6-definitive-all-alive')
def sprunki_phase_6_definitive_all_alive():
    faq_data = get_faqs_for_page('sprunki-phase-6-definitive-all-alive')
    return render_template('game-template.html',
                         page_title='Sprunki Phase 6 Definitive All Alive',
                         page_slug='sprunki-phase-6-definitive-all-alive',
                         faq_data=faq_data)

@app.route('/sprunki-phase-6-definitive-remaster')
def sprunki_phase_6_definitive_remaster():
    faq_data = get_faqs_for_page('sprunki-phase-6-definitive-remaster')
    return render_template('game-template.html',
                         page_title='Sprunki Phase 6 Definitive Remaster',
                         page_slug='sprunki-phase-6-definitive-remaster',
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
    return render_template('game-template.html',
                         page_title='Sprunki Phase 6 Definitive',
                         page_slug='sprunki-phase-6-definitive',
                         faq_data=faq_data)

@app.route('/sprunki-sploinkers')
def sprunki_sploinkers():
    faq_data = get_faqs_for_page('sprunki-sploinkers')
    return render_template('game-template.html',
                         page_title='Sprunki Sploinkers',
                         page_slug='sprunki-sploinkers',
                         faq_data=faq_data)

@app.route('/sprunki-pyramixed-regretful')
def sprunki_pyramixed_regretful():
    faq_data = get_faqs_for_page('sprunki-pyramixed-regretful')
    return render_template('game-template.html',
                         page_title='Sprunki Pyramixed Regretful',
                         page_slug='sprunki-pyramixed-regretful',
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
    return render_template('game-template.html',
                         page_title='Sprunki Sprunkr',
                         page_slug='sprunki-sprunkr',
                         faq_data=faq_data)

@app.route('/sprunki-brud-edition-finale')
def sprunki_brud_edition_finale():
    faq_data = get_faqs_for_page('sprunki-brud-edition-finale')
    return render_template('game-template.html',
                         page_title='Sprunki Brud Edition Finale',
                         page_slug='sprunki-brud-edition-finale',
                         faq_data=faq_data)

@app.route('/sprunki-spruted')
def sprunki_spruted():
    faq_data = get_faqs_for_page('sprunki-spruted')
    return render_template('game-template.html',
                         page_title='Sprunki Spruted',
                         page_slug='sprunki-spruted',
                         faq_data=faq_data)

@app.route('/sprunki-spfundi')
def sprunki_spfundi():
    faq_data = get_faqs_for_page('sprunki-spfundi')
    return render_template('game-template.html',
                         page_title='Sprunki Spfundi',
                         page_slug='sprunki-spfundi',
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
    return render_template('game-template.html',
                         page_title='Sprunki Angry',
                         page_slug='sprunki-angry',
                         faq_data=faq_data)


@app.route('/sprunki-phase-777-3-7')
def sprunki_phase_777_3_7():
    faq_data = get_faqs_for_page('sprunki-phase-777-3-7')
    return render_template('game-template.html',
                         page_title='Sprunki Phase 777 3 7',
                         page_slug='sprunki-phase-777-3-7',
                         faq_data=faq_data)

@app.route('/god-simulator')
def god_simulator():
    faq_data = get_faqs_for_page('god-simulator')
    return render_template('god-simulator.html',
                         page_title='God Simulator',
                         faq_data=faq_data)

@app.route('/dadish')
def dadish():
    faq_data = get_faqs_for_page('dadish')
    return render_template('dadish.html',
                         page_title='Dadish',
                         faq_data=faq_data)

@app.route('/flying-kong')
def flying_kong():
    faq_data = get_faqs_for_page('flying-kong')
    return render_template('flying-kong.html',
                         page_title='Flying Kong',
                         faq_data=faq_data)

@app.route('/ssspicy')
def ssspicy():
    faq_data = get_faqs_for_page('ssspicy')
    return render_template('ssspicy.html',
                         page_title='Ssspicy',
                         faq_data=faq_data)

@app.route('/sprunklings')
def sprunklings():
    faq_data = get_faqs_for_page('sprunki-sprunklings')
    return render_template('game-template.html',
                         page_title='Sprunki Sprunklings',
                         page_slug='sprunklings',
                         faq_data=faq_data)

@app.route('/sprunki-swap-retextured')
def sprunki_swap_retextured():
    faq_data = get_faqs_for_page('sprunki-swap-retextured')
    return render_template('game-template.html',
                         page_title='Sprunki Swap Retextured',
                         page_slug='sprunki-swap-retextured',
                         faq_data=faq_data)

@app.route('/sprunki-upin-ipin')
def sprunki_upin_ipin():
    faq_data = get_faqs_for_page('sprunki-upin-ipin')
    return render_template('game-template.html',
                         page_title='Sprunki Upin Ipin',
                         page_slug='sprunki-upin-ipin',
                         faq_data=faq_data)

@app.route('/sprunki-ultimate-deluxe')
def sprunki_ultimate_deluxe():
    faq_data = get_faqs_for_page('sprunki-ultimate-deluxe')
    return render_template('game-template.html',
                         page_title='Sprunki Ultimate Deluxe',
                         page_slug='sprunki-ultimate-deluxe',
                         faq_data=faq_data)

@app.route('/sprunki-phase-19-update')
def sprunki_phase_19_update():
    faq_data = get_faqs_for_page('sprunki-phase-19-update')
    return render_template('game-template.html',
                         page_title='Sprunki Phase 19 Update',
                         page_slug='sprunki-phase-19-update',
                         faq_data=faq_data)

@app.route('/sprunki-phase-1-7')
def sprunki_phase_1_7():
    faq_data = get_faqs_for_page('sprunki-phase-1-7')
    return render_template('game-template.html',
                         page_title='Sprunki Phase 1 7',
                         page_slug='sprunki-phase-1-7',
                         faq_data=faq_data)

@app.route('/sprunki-dx')
def sprunki_dx():
    faq_data = get_faqs_for_page('sprunki-dx')
    return render_template('game-template.html',
                         page_title='Sprunki Dx',
                         page_slug='sprunki-dx',
                         faq_data=faq_data)

@app.route('/sprunki-banana')
def sprunki_banana():
    faq_data = get_faqs_for_page('sprunki-banana')
    return render_template('game-template.html',
                         page_title='Sprunki Banana',
                         page_slug='sprunki-banana',
                         faq_data=faq_data)

@app.route('/sprunki-garnold')
def sprunki_garnold():
    faq_data = get_faqs_for_page('sprunki-garnold')
    return render_template('game-template.html',
                         page_title='Sprunki Garnold',
                         page_slug='sprunki-garnold',
                         faq_data=faq_data)

@app.route('/sprunki-ketchup')
def sprunki_ketchup():
    faq_data = get_faqs_for_page('sprunki-ketchup')
    return render_template('game-template.html',
                         page_title='Sprunki Ketchup',
                         page_slug='sprunki-ketchup',
                         faq_data=faq_data)

@app.route('/sprunki-agents')
def sprunki_agents():
    faq_data = get_faqs_for_page('sprunki-agents')
    return render_template('game-template.html',
                         page_title='Sprunki Agents',
                         page_slug='sprunki-agents',
                         faq_data=faq_data)

@app.route('/sprunki-banana-porridge')
def sprunki_banana_porridge():
    faq_data = get_faqs_for_page('sprunki-banana-porridge')
    return render_template('game-template.html',
                         page_title='Sprunki Banana Porridge',
                         page_slug='sprunki-banana-porridge',
                         faq_data=faq_data)

@app.route('/sprunki-retake-but-human')
def sprunki_retake_but_human():
    faq_data = get_faqs_for_page('sprunki-retake-but-human')
    return render_template('game-template.html',
                         page_title='Sprunki Retake But Human',
                         page_slug='sprunki-retake-but-human',
                         faq_data=faq_data)

@app.route('/sprunki-retake-new-human')
def sprunki_retake_new_human():
    faq_data = get_faqs_for_page('sprunki-retake-new-human')
    return render_template('game-template.html',
                         page_title='Sprunki Retake New Human',
                         page_slug='sprunki-retake-new-human',
                         faq_data=faq_data)

@app.route('/sprunki-grown-up')
def sprunki_grown_up():
    faq_data = get_faqs_for_page('sprunki-grown-up')
    return render_template('game-template.html',
                         page_title='Sprunki Grown Up',
                         page_slug='sprunki-grown-up',
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

if __name__ == '__main__':
    app.run(debug=True, port=5006)
