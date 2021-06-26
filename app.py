from flask import Flask, redirect, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)