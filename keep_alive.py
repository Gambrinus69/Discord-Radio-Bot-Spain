from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "¡Estoy vivo! <br><br> Lista de radios:<br> - RockFM<br> - KissFM<br> - M80<br> - MaximaFM"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
