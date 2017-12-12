from flask import Flask, render_template, jsonify, request, json, make_response
import requests, redis
from werkzeug.utils import secure_filename
from random import randint
from functools import wraps

app = Flask(__name__)

count = 1
idPlayer = 1000
x1 = 100
x2 = 500
y1 = 350
y2 = 50
directionP1 = 'right'
directionP2 = 'left'
fire1ButtonP1 = 0
fire1ButtonP2 = 0
p1Confirmed = 0
p2Confirmed = 0
gameStart = 0
gameDashboard = [
    {
        'sessionID' : count,
        'cliente1' : None,
        'cliente2' : None,
        'ganadorPartida1' : None,
        'ganadorPartida2' : None,
        'ganadorPartida3' : None,
        'ganadorDelSet' : None
    }]

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'username' and auth.password == 'password':
            return f(*args, **kwargs)
        return make_response('No se pudo verificar su identidad',  401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated

@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/gameReady/', methods=['POST', 'GET', 'PUT'])
def gameReady():
    #chequea en la vase de datos
    #si ciente uno esta lleno
    #si cliente dos esta lleno
    #si ambos lleno devolver ready sino notReady
    return jsonify({'game' : 'ready'})

@app.route('/confirmedReady/', methods=['POST', 'GET', 'PUT'])
def cc():
    global p1Confirmed, p2Confirmed, gameStart
    responseFromClient = request.get_json(force=True)
    print(responseFromClient)
    conf = responseFromClient['confirmed']
    if conf == 1:
        p1Confirmed = 1
    elif conf ==2:
        p2Confirmed = 1
    if p1Confirmed == 1 and p2Confirmed == 1:
        gameStart = 1
        return jsonify({'confirmed':'ready'})

    return jsonify({'confirmed':'notReady'})

@app.route('/setId/', methods=['POST', 'GET', 'PUT'])
def cicloDecision():
    global idPlayer
    if gameDashboard[len(gameDashboard) - 1]['cliente1'] == None:
        gameDashboard[len(gameDashboard) - 1]['cliente1'] = idPlayer
        return jsonify({'getPlayerId': gameDashboard[len(gameDashboard) - 1]['cliente1'], 'getPlayerNum' : 1})
    elif gameDashboard[len(gameDashboard) - 1]['cliente2'] == None:
        gameDashboard[len(gameDashboard) - 1]['cliente2'] = idPlayer+1
        return jsonify({'getPlayerId': gameDashboard[len(gameDashboard) - 1]['cliente2'], 'getPlayerNum' : 2})
    else:
        idPlayer += 2
        gameDashboard.append({
            'sessionID': len(gameDashboard) + 1,
            'cliente1': None,
            'cliente2': None,
            'ganadorPartida1': None,
            'ganadorPartida2': None,
            'ganadorPartida3': None,
            'ganadorDelSet': None
        })
        return cicloDecision()

@app.route('/getP2PositionSet/', methods=['POST', 'GET', 'PUT'])
def p2Set():
    global x2, directionP2, y2, gameStart
    if gameStart == 1:
        #substrae de la base de datos
        if directionP2 == 'right':
            if(x2 < 600):
                x2 += 15
                #y1 -= 5
        elif directionP2 == 'left':
            if (x2 > 0):
                x2 -= 15
               # y1 -= 5
        elif directionP2 == 'up':
            if (y2 > 25):
                #x1 -= -5
                y2 -= 15
        elif directionP2 == 'down':
            if (y2 < 600):
                #x1 -= -5
                y2 += 15
        #if x1 == 400:
         #   x1= 10
        print(directionP2)
        print('This is Y2: '+str(y2))
        print('This is X2: ' + str(x2))
    return jsonify({'x':x2, 'y':y2})

@app.route('/getP1PositionSet/', methods=['POST', 'GET', 'PUT'])
def p1Set():
    global x1, directionP1, y1, gameStart
    if gameStart == 1:
        #substrae de la base de datos
        if directionP1 == 'right':
            if(x1 < 600):
                x1 += 15
                #y1 -= 5
        elif directionP1 == 'left':
            if (x1 > 0):
                x1 -= 15
               # y1 -= 5
        elif directionP1 == 'up':
            if (y1 > 25):
                #x1 -= -5
                y1 -= 15
        elif directionP1 == 'down':
            if (y1 < 600):
                #x1 -= -5
                y1 += 15
        #if x1 == 400:
         #   x1= 10
        print(directionP1)
        print('This is Y: '+str(y1))
        print('This is X: ' + str(x1))
    return jsonify({'x':x1, 'y':y1})

@app.route('/getP1PositionGet/', methods=['POST', 'GET', 'PUT'])
def p1Get():
    global x1, y1
    print(directionP1)
    print('I will give Y: '+str(y1))
    print('I will give X: ' + str(x1))
    return jsonify({'x':x1, 'y':y1})

@app.route('/getP2PositionGet/', methods=['POST', 'GET', 'PUT'])
def p2Get():
    global x2, y2
    print(directionP2)
    print('I will give Y: '+str(y2))
    print('I will give X: ' + str(x2))
    return jsonify({'x':x2, 'y':y2})

@app.route('/hitPlatformP1/', methods=['POST', 'GET', 'PUT'])
def h1Set():
    global x1, directionP1, y1
    responseFromClient = request.get_json(force=True)
    print(responseFromClient)
    directionP1 = responseFromClient['direction']
    x1 = responseFromClient['x']
    y1 = responseFromClient['y']
    if directionP1 == 'up':
        if(y1 < 600):
            y1 += 5
    elif directionP1 == 'down':
        if (y1 >= 25):
            y1 -= 5
    elif directionP1 == 'left':
        if (x1 < 600):
            x1 += 5
    elif directionP1 == 'right':
        if (x1 >= 0):
            x1 -= 5
    directionP1 = setDirection(directionP1)
    print('pegue con algo')
    #guardaria aqui en la base de datos
    return jsonify({'x':222222})

@app.route('/gunShot/', methods=['POST', 'GET', 'PUT'])
def shotSet():
    global fire1ButtonP1,fire1ButtonP2, y1,y2,x1,x2
    if(-13 < (y2 - y1) < 13):
        fire1ButtonP1 = 1
    elif(-13 < (x2 - x1) < 13):
        fire1ButtonP1 = 1
    else:
        fire1ButtonP1 = 0

    if(-13 < (y1 - y2) < 13):
        fire1ButtonP2 = 1
    elif(-13 < (x1 - x2) < 13):
        fire1ButtonP2 = 1
    else:
        fire1ButtonP2 = 0
    return jsonify({'fire1ButtonP1': fire1ButtonP1, 'fire1ButtonP2' : fire1ButtonP2})

@app.route('/hitPlatformP2/', methods=['POST', 'GET', 'PUT'])
def h2Set():
    global x2, directionP2, y2
    responseFromClient = request.get_json(force=True)
    print(responseFromClient)
    directionP2 = responseFromClient['direction']
    x2 = responseFromClient['x']
    y2 = responseFromClient['y']
    if directionP2 == 'up':
        if(y2 < 600):
            y2 += 5
    elif directionP2 == 'down':
        if (y2 >= 25):
            y2 -= 5
    elif directionP2 == 'left':
        if (x2 < 600):
            x2 += 5
    elif directionP2 == 'right':
        if (x2 >= 0):
            x2 -= 5
    directionP2 = setDirection(directionP2)
    print('pegue con algo P2')
    #guardaria aqui en la base de datos
    return jsonify({'x':222222})

def setDirection(direction):
    randomNum = randint(0, 3)
    newDirection = ''
    if randomNum == 0:
        newDirection = 'right'
    elif randomNum == 1:
        newDirection = 'left'
    elif randomNum == 2:
        newDirection = 'up'
    elif randomNum == 3:
        newDirection = 'down'
    print('Nueva direccion: '+newDirection)
    if newDirection == direction:
        return setDirection(direction)
    return  newDirection

@app.route('/getfile', methods=['GET', 'POST'])
def getfile():
    if request.method == 'POST':
        cVerbos, cConjunciones, cPronombres, cArticulos = inicializarContadores()
        test = request.files['myfile']
        r_server = redis.Redis("192.168.0.14")
        data = test.readlines();
        for line in data:
            words = line.split()
            for word in words:
                wordRaw = str(word.decode('latin-1')).lower()
                if r_server.exists(wordRaw):
                    tipo = r_server.get(wordRaw).decode('latin-1')
                    cVerbos2, cConjunciones2, cPronombres2, cArticulos2 = verificar(tipo)
                    print(cVerbos2, cConjunciones2, cPronombres2, cArticulos2)
                    cVerbos += cVerbos2
                    cConjunciones += cConjunciones2
                    cPronombres += cPronombres2
                    cArticulos += cArticulos2
                else:
                    print('does not exist')


        return render_template("chart.html", cVerbos=cVerbos, cConjunciones=cConjunciones,cPronombres=cPronombres, cArticulos=cArticulos)
    else:
        return 'ERROR, metodo utilizado para acceder no es reconocido'

def verificar(tipo):
    cVerbos, cConjunciones, cPronombres, cArticulos = 0,0,0,0
    if tipo == 'verbos':
        cVerbos = 1
    elif tipo == 'articulos':
        cArticulos = 1
    elif tipo == 'conjunciones':
        cConjunciones = 1
    elif tipo == 'pronombres':
        cPronombres = 1
    return cVerbos, cConjunciones,cPronombres,cArticulos

def inicializarContadores():
    cVerbos = 0;
    cConjunciones = 0;
    cPronombres = 0;
    cArticulos = 0;
    return cVerbos, cConjunciones,cPronombres,cArticulos

@app.route('/')
@requires_auth
def hello():
    return render_template("tanks.html")

if __name__ == '__main__':
    app.run()