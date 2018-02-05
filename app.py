# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:54:38 2018

@author: Saniyah
"""

from flask import Flask, render_template, request
from backend import parse_recipes as parser
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

@app.route('/submitInput', methods=['POST'])
def submitInput():
    # read the posted values from the UI
    # return render_template('submitted.html', item = "test", num = "3", meas = "cup")
    try:
        name = request.form['inputItem']
        num = request.form['inputQuantity']
        meas = request.form['inputMeasurement']
 
        # validate the received values
        if name and num and meas: 
            return render_template('submitted.html', item = str(name), num = str(num), meas = str(meas))
        else:
            return render_template('error.html', error = "Error getting inputs")
    
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route("/")
@app.route("/main")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
    
    