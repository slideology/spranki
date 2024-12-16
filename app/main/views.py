from flask import render_template, send_from_directory
from . import main
from .. import cache
from ..utils.seo import SEOHelper

seo_helper = SEOHelper()

@main.route('/')
@cache.cached(timeout=300)
def home():
    meta = seo_helper.get_page_metadata()["home"]
    return render_template('index.html',
                         meta_tags=seo_helper.get_meta_tags(**meta),
                         title=meta["title"])

@main.route('/about')
@cache.cached(timeout=300)
def about():
    meta = seo_helper.get_page_metadata()["about"]
    return render_template('about.html',
                         meta_tags=seo_helper.get_meta_tags(**meta),
                         title=meta["title"])

@main.route('/game')
@cache.cached(timeout=300)
def game():
    meta = seo_helper.get_page_metadata()["game"]
    return render_template('game.html',
                         meta_tags=seo_helper.get_meta_tags(**meta),
                         title=meta["title"])

@main.route('/coloring')
@cache.cached(timeout=300)
def coloring():
    meta = seo_helper.get_page_metadata()["coloring"]
    return render_template('coloring.html',
                         meta_tags=seo_helper.get_meta_tags(**meta),
                         title=meta["title"])

@main.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@main.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')
