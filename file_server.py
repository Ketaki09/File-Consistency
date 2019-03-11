import socket
import time
all_connections = []
all_address = []


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


def accepting_connections():
    results = ''
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:

        try:
            if len(all_connections) is not 3:
                conn, address = s.accept()
                s.setblocking(1)  # prevents timeout

                all_connections.append(conn)
                all_address.append(address)

                print("Connection has been established!" + "IP" + address[0] + ":" + str(address[1]))

            else:
                for i, conn in enumerate(all_connections):
                    print("in loop accepting_connections")
                    conn.send(str.encode(str(i)))
                    s.setblocking(1)  # prevents timeout
                    conn.recv(4096)
                    results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"
                    print("----Clients----" + "\n" + results)

                search_flags(all_connections)

        except:
            print("Error accepting connections")


def search_flags(all_connections):
    while True:
        # try:
        for i, conn in enumerate(all_connections):
            conn.send(str.encode(" "))
            data = conn.recv(4096)
            s.setblocking(1)  # prevents timeout

            if data[:].decode("utf-8") == '0' or data[:].decode("utf-8") == '1' or data[:].decode("utf-8") == '2':
                client_update_file_number = data[:].decode("utf-8")
                # print(client_update_file_number)
                with open('k_server.txt', 'wb') as f:
                    print ("File opened")
                    update_data = conn.recv(4096)
                    # if not update_data:
                    #     break
                    f.write(update_data)
                    print("The file has been modified")

                f.close()
                send_data_to_clients(all_connections, client_update_file_number)

            # if data[:].decode("utf-8") == '10' or data[:].decode("utf-8") == '11' or data[:].decode("utf-8") == '12':
            #     client_disconnect = data[:].decode("utf-8")
            #     client_disconnect = int(client_disconnect)
            #     all_connections.pop(client_disconnect)
            #     print(client_disconnect)


        # except socket.error as msg:
        #     print("Seraching flag  error" + str(msg) + "\n" + "Retrying...")
        #     search_flags(all_connections)


def send_data_to_clients(all_connections, client_update_file_number):
    print(client_update_file_number)
    for i, connection in enumerate(all_connections):
        if connection != all_connections[int(client_update_file_number)]:
            connection.send(str.encode("The File is changed"))
            filename = 'k_server.txt'
            send_file = open(filename, 'rb')
            variable = send_file.read(4096)
            while variable:
                connection.send(variable)
                print('Sent', repr(variable))
                variable = send_file.read(4096)

            send_file.close()

def main():
    create_socket()
    bind_socket()
    accepting_connections()


main()