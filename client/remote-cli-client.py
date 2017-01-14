from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
import random
import json
import thread
import time
import subprocess
from helpers import *
WLAN_INTERFACE = "wlan0"
ETHERNET_INTERFACE = "eth1"


this_client_room_id = 0
request_client_room_id = 0

device_info = {"wireless_mac" : "" , "ethernet_mac": "" , "hostname" : "" , "os_name": "" , "kernel_version": "", "lan_ip_address":"", "wlan_ip_address":""}


def set_device_info():
    sys_info = get_system_info()
    device_info["wireless_mac"] = get_mac_id(WLAN_INTERFACE)
    device_info["ethernet_mac"] = get_mac_id(ETHERNET_INTERFACE)
    device_info["os_type"] = sys_info["os_type"]
    device_info["hostname"] = sys_info["hostname"]
    device_info["kernel_version"] = sys_info["kernel_version"]
    device_info["arch"] = sys_info["arch"]
    device_info["lan_ip_address"] = get_ip_address(ETHERNET_INTERFACE)
    device_info["wlan_ip_address"] = get_ip_address(WLAN_INTERFACE)
    device_info["os_name"] = get_distribution()
    return

def get_random_number(start=1, end=100):
    return random.randint(start,end)

def send_client_info():
    client_info = {}
    client_id = get_random_number()
    client_info["client_id"] = client_id
    client_info.update(device_info)
    print(client_info)
    print("Client id is %d " %(client_id))
    socketIO.emit("connect_client", client_info)

def on_connect():
    send_client_info()
    print("Connected")


def on_disconnect():
    print('disconnect')

def on_reconnect():
    send_client_info()
    print('reconnect')

def cmd_response(*args):
    print('on chat message ', args)

def handshake(*args):
    global this_client_room_id, request_client_room_id
    this_client_room_id = args[0]
    request_client_room_id = args[1]
    print("Ready to receive direct message from browser", args )

def command(*args):
    print("this is the command to be exxecuted " , args)
    print("len of args is %s" % (len(args)))
    op = execute_a_command(args[0])
    socketIO.emit("command-output", op, request_client_room_id)


def execute_a_command(command):
    try:
        cmd = command.strip().split()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)  # not using shell = True
        process.wait()
        output = process.communicate()[0].strip("\n")
        print("op is **********")
        print(output)
        return output
    except Exception as e:
        return "error in command"


socketIO = SocketIO('localhost', 4000, LoggingNamespace)
socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)
socketIO.on('chat message', cmd_response)
socketIO.on("handshake", handshake)
socketIO.on("command", command)
set_device_info()
# socketIO.on('joinGroup', save_group_id)

# socketIO.emit('aaa')
socketIO.wait()
# socketIO.wait(seconds=1)

