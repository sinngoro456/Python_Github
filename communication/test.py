# coding: utf-8
import socket

# ポート番号とプロトコル名からサービス名を取得
def service_name(port, protocol_name):
    print('Port:', port, '\nprotocolname:', protocol_name)
    print('Service name:', socket.getservbyport(port, protocol_name))
    print('--------------------')

if __name__ == "__main__":
    service_name(port=80, protocol_name='tcp')
    service_name(port=23, protocol_name='tcp')
    service_name(port=25, protocol_name='tcp')