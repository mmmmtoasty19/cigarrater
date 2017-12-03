from flask import Flask

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'dfa111lkjlksfAF097KKLN1231231209SFDFKJASFMN'


@app.route('/')
def index():
    return "Hey it worked!"

if __name__ == "__main__":
    app.run(debug=DEBUG,host=HOST,port=PORT)