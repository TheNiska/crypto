# -*- coding: utf-8 -*-
from app import app
from flask import (render_template, url_for, request, redirect,
                   session, flash, current_app, jsonify)


@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")
