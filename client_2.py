import socket
import os
import subprocess
import os.path, time

alloted_client_no = []

s = socket.socket()
host = '192.168.29.61'
port = 9999

s.connect((host, port))
stat_new = os.path.getmtime("k_1.txt")
stat = os.path.getmtime("k_1.txt")
while True:
    s.setblocking(1)
    data = s.recv(4096)
    s.send(str.encode(" "))

    if not alloted_client_no:
        if data.decode("utf-8") == "0" or data.decode("utf-8") == "1" or data.decode("utf-8") == "2":
            alloted_client_no = data.decode("utf-8")
            s.send(str.encode("Connection received"))
            print(alloted_client_no)

    stat_new = os.path.getmtime("k_1.txt")
    if stat_new != stat:
        print("The file has changed")
        stat = os.path.getmtime("k_1.txt")
        s.send(str.encode(alloted_client_no))
        filename = 'k_1.txt'
        f = open(filename, 'rb')
        l = f.read(4096)
        while (l):
            s.send(l)
            print('Sent', repr(l))
            l = f.read(4096)

        f.close()
        print("The file has been modified by update")

    if data.decode("utf-8") == "The File is changed":
        with open('k_1.txt', 'wb') as file_receive:
            print("File opened")
            update_data = s.recv(4096)
            # if not update_data:
            #     break
            file_receive.write(update_data)
            file_receive.close()
            print("The file has been modified")
            stat_new = os.path.getmtime("k_1.txt")
            stat = os.path.getmtime("k_1.txt")








    # if data[:2].decode("utf-8") == 'cd':
    #     os.chdir(data[3:].decode("utf-8"))
    #
    # if len(data) > 0:
    #     cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    #     output_byte = cmd.stdout.read() + cmd.stderr.read()
    #     output_str = str(output_byte,"utf-8")
    #     currentWD = os.getcwd() + "> "
    #     s.send(str.encode(output_str + currentWD))
    #
    #     print(output_str)


