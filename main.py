from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        paste_content = request.form['paste']
        with open('pastes.txt', 'a') as f:
            f.write(paste_content + '\n')
        return redirect(url_for('index'))
    else:
        with open('pastes.txt', 'r') as f:
            pastes = f.readlines()
        return render_template('index.html', pastes=pastes)

if __name__ == '__main__':
    app.run(debug=True)