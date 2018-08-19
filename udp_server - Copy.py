#!/usr/bin/python3

import sys
from socket import socket, SOCK_DGRAM, AF_INET

def print_error(e, f="UNKNOWN"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))

def recv_data(udp_sock):
  try:
    data, (ip, port) = udp_sock.recvfrom(100)
    print("Received %d bytes" % (len(data)))
    print(data.decode('utf-8'))
  except Exception as e:
    print_error(e, "recvfrom")

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
    udp_sock = socket(AF_INET, SOCK_DGRAM)
  except Exception as e:
    print_error(e, "socket")
  
  try:
    udp_sock.bind((ip, port))
  except Exception as e:
    print_error(e, "bind")
  
  try:
    recv_data(udp_sock)
  except Exception as e:
    print_error(e, "recv_data")

if __name__ == "__main__":
  main()
