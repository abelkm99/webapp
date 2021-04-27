from flask import Flask,request,render_template
import lib
import bluetooth

app = Flask(__name__)

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

address = ["88:1B:99:09:E8:96","88:1B:99:06:CA:16"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect')
def get_address():
    # address = lib.get_address()
    # print(address)
    sock.connect((address[1], 6))
    
    '''
    TODO:
        [] do a function to check if it is connected
    '''
    return "connected succesfully"


@app.route('/singleservo',methods=['POST'])
def print_servoId():
    print('sock here is ',sock)
    req = request.get_json()
    data = []
    for key,value in req.items():
        data.append(value)
    data.append(10)
    data.append(0)
    data = [bytes([int(x)]) for x in data]
    print('sock is ',sock)
    if sock:
        try:
            blueres = lib.send_single_servo(data,sock)
        except:
            pass
    else:
        return "not conneced"
    return "scusse"


@app.route('/multipleservo',methods=['POST'])
def send_multiple_data():
    req = request.get_json()
    req.append(10)
    req.append(0)
    data = [bytes([int(x)]) for x in req]

    blueres = lib.send_multiple_servo(data,sock)
    
    print(blueres)
    return "scusse"



@app.route('/excAction',methods=['POST'])
def excute_action():
    req = request.get_json()
    action = req.get('Action')
    lib.send_action(action,sock)
    return "scusse"