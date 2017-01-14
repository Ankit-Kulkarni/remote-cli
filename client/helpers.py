import fcntl
import struct
import socket
import os
import subprocess
import netifaces as ni
import re

# helpers
def get_version(
                pname, exist_comm, exec_comm,
                filter_exp_1, filter_exp_2):
    '''
    Returns version of the process pname. Takes input params as
    pname --> program name
    exist_comm --> command to check if program exist
    exec_command --> command to get versions of the program
    filter_exp_1 --> expression to filter the version out
    from exec_command output
    filter_exp_2 --> expression to filter the version out
    from exec_command output after filtering from filter_exp_1
    '''
    try:
        process = subprocess.Popen(
            exist_comm.split(), stdout=subprocess.PIPE)
        # check if program exist
        is_pname_exist = process.communicate()[0].strip("\n")
        # if exist process, else tell do not exist

        if is_pname_exist == "":
            return "-"
        else:
            process = subprocess.Popen(
                exec_comm.split(), stdout=subprocess.PIPE)
            pname_version = process.communicate()[0].strip("\n")

            # extract version out of string
            s = re.search(filter_exp_1, pname_version).group(0)
            pname_version = re.search(filter_exp_2, s).group(0)
            return pname_version
    except Exception, e:
        return "-"

# apis
def get_mac_id(ifname):
    ''' get_mac_id(ifname)
    Returns mac id of the interface
    input --> ifname, output --> mac id
    Returns mac Id of given interface
    '''
    # this code is from http://stackoverflow.com/a/4789267
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack(
        '256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])


def get_system_info():
    response = {"os_type": "", "hostname" : "", "kernel_version": "", "arch": "", "error": ""}
    try:
        info = os.uname()
        response["os_type"] = info[0]
        response["hostname"] = info[1]
        response["kernel_version"] = info[2]
        response["arch"] = info[4]
    except Exception as e:
        response["error"] = str(e)

    return response

def get_code_name():
    '''
    Returns  codename for linux
    '''
    return get_version(
        "Codename", "which lsb_release", "lsb_release -c", "\t.*", "\S.*")

def get_distribution():
    '''
    Returns  codename for linux
    '''
    return get_version(
        "Codename", "which lsb_release", "lsb_release -d", "\t.*", "\S.*")

def get_ip_address(ifname):
    """
    get the ip address on the interface ifname
    """
    try:
        # get and return the ip address
        ip_add = ni.ifaddresses(ifname)[2][0]['addr']
        return ip_add
    except KeyError:
        return "Not available"
    except ValueError:
        "valueError"

if __name__ == '__main__':
    ifname1 = "wlan0"
    ifname2 = "eth1"
    print(get_mac_id(ifname1))
    print(get_mac_id(ifname2))
    info = get_system_info()
    if info["os_type"] == "Linux" :
        codename = get_code_name()
        distribution = get_distribution()
    else :
        codename = "Not supported"
        distribution = "Not supported"
    print(distribution + " " + codename )
    print(get_ip_address(ifname1))
    print(get_ip_address(ifname2))
