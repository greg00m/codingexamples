#!/usr/bin/python3

import sys
from socket import socket, SOCK_STREAM, AF_INET
from select import select
import traceback


def print_error(e, f="UNKNOWN"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))
    traceback.print_exc()

def recv_data(tcp_sock):
  try:
    data = tcp_sock.recv(4096)
    # Indicates client has disconnected
    if len(data) == 0:
      return False
    print("Received %d bytes" % (len(data)))
    print(data.decode('utf-8'))
    # Echo the data back to the client
    tcp_sock.send(data)
    return True
  except BlockingIOError as b:
    print("Recv failed due to non-blocking IO, this means the client has disconnected?")
    return False
  except Exception as e:
    print_error(e, "recv")
    return False

def main():
  if len(sys.argv) == 3:
    ip = sys.argv[1]
    try:
      port = int(sys.argv[2])
    except:
      print("Port %s unable to be converted to number, run with HOST PORT" % (sys.argv[2]))
      sys.exit(1)
  else:
    print("Run with %s HOST PORT" % (sys.argv[0]))
    sys.exit(1)

  try:
    server_sock = socket(AF_INET, SOCK_STREAM)
  except Exception as e:
    print_error(e, "socket")
    sys.exit(1)
  
  try:
    server_sock.bind((ip, port))
  except Exception as e:
    print_error(e, "bind")
    sys.exit(1)

  try:
    server_sock.listen(10)
  except Exception as e:
    print_error(e, "listen")
    sys.exit(1)

  read_sockets = []
  write_sockets = []
  except_sockets = []
  
  read_sockets.append(server_sock)
  except_sockets.append(server_sock)
  quit = False

  readlist, writelist, exceptlist = [], [], []

  while (quit == False):
    try:
      readlist, writelist, exceptlist = select(read_sockets, write_sockets, except_sockets)
    except KeyboardInterrupt as k:
      quit = True
    except Exception as e:
      print_error(e, "select")

    if server_sock in readlist:
      try:
        client_sock, (client_ip, client_port) = server_sock.accept()
        client_sock.setblocking(0)
        read_sockets.append(client_sock)
        except_sockets.append(client_sock)
      except KeyboardInterrupt as k:
        quit = True
      except Exception as e:
        print_error(e, "accept")

    for client in read_sockets:
      # Means client has sent us data
      if client in readlist:
        try:
          ret = recv_data(client_sock)
          if ret == False:
            print("Closing client socket.")
            client.close()
            read_sockets.remove(client)
            except_sockets.remove(client)
            break
        except KeyboardInterrupt as k:
          quit = True
        except Exception as e:
          print_error(e, "recv_data")

      if client in exceptlist:
        print("Closing client socket (client in except?).")
        client.close()
        read_sockets.remove(client)
        except_sockets.remove(client)
  try:
    print("Closing sockets.")
    server_sock.close()
    for client_sock in read_sockets:
      client_sock.close()
  except:
    pass
if __name__ == "__main__":
  main()
