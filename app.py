#flask/bin/python
from flask import Flask, jsonify, request
from lamp import *
from guilamp import *
from consumption import *
from networkConsumptionObserver import *

app = Flask(__name__)
lp = LampStrut()
consumption = LampConsumption(lp)

@app.route('/')
def index():
  return jsonify(lp.getJson())

@app.route('/services/ligar', methods=['GET'])
def ligar():
  lp.callService('ligar')
  return jsonify(lp.getJsonStatus())

@app.route('/services/desligar', methods=['GET'])
def desligar():
  lp.callService('desligar')
  return jsonify(lp.getJsonStatus())

@app.route('/services/definir_brilho', methods=['GET'])
def set_bright():
  lp.callService('definir_brilho', request.args)
  return jsonify(lp.getJsonStatus())

@app.route('/services', methods=['GET'])
def getServices():
  return jsonify(lp.getJsonServices())

@app.route('/status', methods=['GET'])
def status():
  return jsonify(lp.getJsonStatus())

@app.route('/consumption', methods=['GET'])
def consumptionHistory():
  return jsonify({"consumption" : consumption.getConsumptionHistory()})

@app.route('/register_notifier', methods=['GET'])
def registerNotifier():
  consumption.addConsumptionObserver(NetworkConsumptionObserver(request.args))
  return jsonify({"response" : "ok"})

#TODO: como remover observer??



if __name__ == '__main__':
  gui = GuiLamp(1, lp)
  gui.start()

  consumption.start()

  app.config['SERVER_NAME'] = 'localhost:5000'
  app.run(debug=True, use_reloader=False)

  #stop other threads
  gui.stop()
  consumption.stop()
  gui.join()
  consumption.join()
  
