from flask import Flask, redirect, request, abort
from UrlShortener import app, cache
import psycopg2
import string
import random
import json
from flask_cache import Cache

conn = psycopg2.connect("host=elmer-02.db.elephantsql.com port=5432 user=fljoirkd password=ba3xgTrI78G3GKUbyD6hNyRU_HBKXOXn dbname=fljoirkd")
cur = conn.cursor()

@app.route('/url/<short_url>')
@cache.memoize()
def redirect_to_original_url(short_url=''):
    """Redirects to the original url"""        
    cur.execute("SELECT * FROM links WHERE id = %s", (short_url,))
    try:
        res = cur.fetchone()
        return redirect(res[1], code=302)
    except:
        abort(404)
    

@app.route('/add_url', methods=['POST'])
def add_url():
    """Adds url to the DB""" 
    # check if the post request has url file part
    if 'url' not in request.form or  request.form['url'] == '':
        flash('No url')
        return redirect(request.url)
    id=gen_id()
    cur.callproc("sp_add_link", (id, request.form['url']))
    short_url = cur.fetchone()[0]
    conn.commit()
    if short_url == None:
        short_url = id;
    return json.dumps({'success':True, 'url':short_url}), 200, {'ContentType':'application/json'} 

def gen_id():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))