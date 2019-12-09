from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        if(str(request.form['user']) == "dodare"
        && str(request.form['password']) == "sdn") {
            return render_template('signin.html')
        }
        else {
            return render_template('index.html')
        }
    else:
        return render_template('index.html')

