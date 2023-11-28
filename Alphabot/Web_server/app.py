from flask import Flask, render_template, request
import AlphaBot
from time import sleep
app = Flask(__name__)

piero = AlphaBot.AlphaBot()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #print(request.form.get('avanti'))
        if request.form.get('avanti') == 'avanti':
            piero.forward()
            sleep(1)
            piero.stop()
        elif  request.form.get('indietro') == 'indietro':
            piero.backward()
            sleep(1)
            piero.stop()
        elif  request.form.get('sinistra') == 'sinistra':
            piero.left()
            sleep(1)
            piero.stop()
        elif  request.form.get('destra') == 'destra':
            piero.left()
            sleep(1)
            piero.stop()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')