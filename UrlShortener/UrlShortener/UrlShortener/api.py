from flask import Flask, redirect, request
from UrlShortener import app

@app.route('/<short_url>')
def redirect_to_original_url(short_url=''):
    """Redirects to the original url"""
    return redirect("http://google.com", code=302)