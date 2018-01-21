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
def showInput():
    return render_template('input.html')

@app.route('/showPantry')
def showPantry():
    return render_template('pantry.html')

@app.route('/showFilter')
def showFilter():
    return render_template('filter.html')

@app.route('/submitInput', methods=['GET', 'POST'])
def submitInput():
     # read the posted values from the UI
    name = request.form['inputName']
    num = request.form['inputNumber']
    meas = request.form['inputMeasurement']
 
    # validate the received values
    if name and num and meas:
        return render_template('submitted.html')
    else:
        return render_template('404.html')

@app.route("/")
@app.route("/main")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
    
    