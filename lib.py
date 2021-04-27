import bluetooth

action_list = {
    'forward':'Move forward',
    'back':'Move back',
    'left':'Move Leftward',
    'right':'Move Rightward',
    'rpunch':'Right punch',
    'lpunch':'Left punch',
    'tleft':'Turn Left',
    'tright':'Turn Right',
    'default':'',
    'getup':'get up',


}

def discover():
    print("searching ...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))
    print(nearby_devices)
    
    for addr, name in nearby_devices:
        if name == "Alpha1_E896":
            return addr


def get_address():
    bd_addr = None
    counter = 1
    while (bd_addr is None):
        print('attempt',counter)
        counter+=1
        bd_addr = discover()

    port = 6
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    return bd_addr


def create_message(command,parameters):
    header = b'\xFB\xBF'
    end = b'\xED'
    parameter = b''.join(parameters)
    length = bytes([len(parameters)+5])
    data = [command, length]
    data.extend(parameters)
    
    print(data)
    
#     total = [sum((ord(x)) for x in data)]
    
    total = 0
    for x in data:
        total += ord(x)
        total %= 256    
    print (total)
    check = bytes([total])
    return header+length+command+parameter+check+end


def single_servo_command(servo_id,angle,runtime,frame_interval=0):
    if servo_id < 1 or servo_id>16:
        print("the servo id doesn't exist")
        return None
    param = [servo_id,angle,runtime,frame_interval]
    param = [(x).to_bytes(1, byteorder='big') for x in param]
    return param


def send_single_servo(data,sock):
    msg = create_message(b'\x22', data)
    sock.send(msg)
    rres = sock.recv(1024)
    return rres


def send_multiple_servo(data,sock):
    msg = create_message(b'\x23', data)
    sock.send(msg)
    rres = sock.recv(1024)
    return rres

def send_action(action,sock):
    data  = action_list.get(action)
    print(data)
    data = bytes(data,'ascii')
    data = [(x).to_bytes(1,'big') for x in data]
    print(data)
    msg = create_message(b'\x03',data)
    print(msg)
    sock.send(msg)
    rres = sock.recv(1024)
    return rres