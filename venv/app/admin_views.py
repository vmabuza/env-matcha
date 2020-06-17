from flask import Flask,render_template,url_for,flash,g, redirect,session,request,make_response
from app import app


@app.route('/admin/dashboard')
def dash_board():
    return render_template('admin/dash_board.html')

@app.route('/about')
def about():
    return 'About'