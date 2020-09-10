"Simple=HTTP Methods"
from socket import socket, getaddrinfo, AF_INET
import ssl
import os.path
import socket


def http_get(url, overwrite=False):
    """ simple http method get request """
    _, _, host, path = url.split('/', 3)
    filename = url.split('/')[-1]
    if 'https' in url:
      port = 443
    else:
      port = 80
    addr = getaddrinfo(host, port)[0][-1]
    if os.path.exists(os.path.abspath(os.path.join(os.path.curdir, filename))):
        if overwrite:
            print('overwriting...\r\n')
            print('--------------------')
            print('\r\n')
        else:
            filename = filename + 'new'
            print('writing to: %s\r\n' % filename)

#    conn = socket.socket()
    addr = getaddrinfo(host, port)[0][-1]
#    context = ssl.create_default_context()
#    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    with socket.create_connection((host, 443)) as sock:
      print(sock)
      with context.wrap_socket(sock, server_hostname=host) as ssock:
        print(ssock.version())
#        conn = ssock.connect((host, port), 1024)
        #ssock.connect(1024)
        ssock.sendall(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        with open(filename, 'wb') as f:
            while True:
                data = ssock.recv(1024)
                if data:
                      f.write(bytes(str(data), encoding='utf8', errors='ignore'))
                else:
                    break
#    conn.close()
#        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
#        context.verify_mode = ssl.CERT_REQUIRED
#        context.check_hostname = True
#        context.load_verify_locations('../certs/demoCA/private/cacert-test-tsakey.pem')
#        context.load_cert_chain(certfile="../certs/cert.pem", keyfile="../certs/key.pem")
#        context.load_verify_locations("../certs/demoCA/localhost.crt")
#        context.load_default_certs()

       # ssl_sock = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
 #       ssock.connect((host, port))

#        conn = context.wrap_socket(socket(AF_INET), server_hostname=host)


if __name__ == '__main__':
    try:
        from sys import argv
        http_get(argv[1])
    except ImportError:
        http_get('https://www.python.org/')
