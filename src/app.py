from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return 'Welcome to Squawk'

@app.route('/restaurants')
def restaurants():
    return 'chipotle, sweetgreen, and five guys'
