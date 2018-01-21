# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:54:38 2018

@author: Saniyah
"""

from flask import Flask, render_template, request
app = Flask(__name__)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/showInput')
def showSignUp():
    return render_template('input.html')


@app.route('/submitInput', methods=['GET', 'POST'])
def submitInput():
    return render_template('submitted.html')

@app.route("/")
@app.route("/main")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
    
    