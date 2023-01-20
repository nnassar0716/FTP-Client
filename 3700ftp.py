
from urllib.parse import urlparse
import argparse
import socket
import os

my_parser = argparse.ArgumentParser(description="Communicate with an FTP server")
my_parser.add_argument("operation", help="The operation being done", type=str)
my_parser.add_argument("params", help="Parameters for the given operation. Will be one or two paths and/or URLs.",
                       type=str, nargs='+')
args = my_parser.parse_args()

operation = args.operation
params = args.params

if len(params) == 2:
    if "ftp:" in params[0]:
        parsed_url = urlparse(params[0])
        username = parsed_url.username
        password = parsed_url.password
        host_name = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path
        local_path = params[1]
    else:
        parsed_url = urlparse(params[1])
        username = parsed_url.username
        password = parsed_url.password
        host_name = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path
        local_path = params[0]
else:
    parsed_url = urlparse(params[0])
    username = parsed_url.username
    password = parsed_url.password
    host_name = parsed_url.hostname
    port = parsed_url.port
    path = parsed_url.path

user_command = "USER " + username + "\r\n"
pass_command = "PASS " + password + "\r\n"
type_command = "TYPE I\r\n"
mode_command = "MODE S\r\n"
stru_command = "STRU F\r\n"
quit_command = "QUIT\r\n"

control_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

control_channel.connect((host_name, port))
received_data = control_channel.recv(8100).decode()
print(received_data)


def send_receive_control(command):
    control_channel.send(command.encode())
    received = control_channel.recv(8100).decode()
    print(received)


def setup_server():
    send_receive_control(user_command)
    send_receive_control(pass_command)
    send_receive_control(type_command)
    send_receive_control(mode_command)
    send_receive_control(stru_command)


def get_second_port(passive_string):
    first_parentheses_remove = passive_string.replace("227 Entering Passive Mode (", "")
    second_parentheses_remove = first_parentheses_remove.replace(").", "")
    list_of_ints = list(map(int, second_parentheses_remove.split(",")))
    top_bit, bottom_bit = list_of_ints[4], list_of_ints[5]
    second_port = top_bit << 8 | bottom_bit
    return second_port


def get_ip_address(passive_string):
    first_parentheses_remove = passive_string.replace("227 Entering Passive Mode (", "")
    second_parentheses_remove = first_parentheses_remove.replace(").", "")
    list_of_ints = second_parentheses_remove.split(",")
    ip = list_of_ints[0] + "." + list_of_ints[1] + "." + list_of_ints[2] + "." + list_of_ints[3]
    return ip


def passive_command():
    pasv_command = "PASV\r\n"
    control_channel.send(pasv_command.encode())
    received = control_channel.recv(8100).decode()
    print(received)
    second_port = get_second_port(received)
    ip = get_ip_address(received)
    data_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_channel.connect((ip, second_port))
    if operation == "ls":
        list_command = "LIST " + path + "\r\n"
        control_channel.send(list_command.encode())
        received = data_channel.recv(8100).decode()
        print(received)
        data_channel.close()
    elif operation == "cp" and "ftp:" in params[1]:
        store_command = "STOR " + path + "\r\n"
        control_channel.send(store_command.encode())
        received = control_channel.recv(8100).decode()
        print(received)
        file = open(local_path).read()
        data_channel.send(bytes(file.encode()))
        data_channel.close()
        received = control_channel.recv(8100).decode()
        print(received)
        send_receive_control(quit_command)
    elif operation == "cp" and "ftp:" in params[0]:
        return_command = "RETR " + path + "\r\n"
        control_channel.send(return_command.encode())
        control_channel.recv(8100).decode()
        received = data_channel.recv(8100)
        with open(local_path, 'wb') as file:
            file.write(received)
        data_channel.close()
        send_receive_control(quit_command)
    elif operation == "mv" and "ftp:" in params[1]:
        store_command = "STOR " + path + "\r\n"
        control_channel.send(store_command.encode())
        received = control_channel.recv(8100).decode()
        print(received)
        file = open(local_path).read()
        data_channel.send(bytes(file.encode()))
        data_channel.close()
        received = control_channel.recv(8100).decode()
        print(received)
        os.remove(local_path)
        send_receive_control(quit_command)
    elif operation == "mv" and "ftp:" in params[0]:
        return_command = "RETR " + path + "\r\n"
        control_channel.send(return_command.encode())
        control_channel.recv(8100).decode()
        received = data_channel.recv(8100)
        with open(local_path, 'wb') as file:
            file.write(received)
        delete_command()
        data_channel.close()
        send_receive_control(quit_command)


def delete_command():
    dele_command = "DELE " + path + "\r\n"
    send_receive_control(dele_command)


def mkdir_command():
    mkd_command = "MKD " + path + "\r\n"
    send_receive_control(mkd_command)


def rmdir_command():
    rmd_command = "RMD " + path + "\r\n"
    send_receive_control(rmd_command)


setup_server()

if operation == "ls" or "mv" or "cp":
    passive_command()

if operation == "mkdir":
    mkdir_command()
    send_receive_control(quit_command)

if operation == "rmdir":
    rmdir_command()
    send_receive_control(quit_command)

if operation == "rm":
    delete_command()
    send_receive_control(quit_command)

