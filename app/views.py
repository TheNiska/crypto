# -*- coding: utf-8 -*-
from app import app
from flask import (render_template, url_for, request, redirect,
                   session, flash, current_app, jsonify)
from app.controller import get_blocks


@app.route('/', methods=['GET'])
def home():
    blocks = get_blocks(db_path="app/blockchain.db")
    return render_template("home.html", blocks=blocks)
