"Simple=HTTP Methods"
from socket import socket, getaddrinfo, AF_INET
from io import BytesIO
from ssl import create_default_context
from os.path import getmtime, getatime, getctime, exists, curdir, split, join, pathsep, abspath
import json


def http_get(url):
    """ simple http method get request """
    _, _, host, path = url.split('/', 3)
    filename = url.split('/')[-1]
    name = abspath(join(curdir, filename))
    if exists(name):
        name = abspath(join(curdir, str(getmtime(name)) + '_' + filename))
        print('Creating new at:\r\n {}\r\n'.format(name))

    if 'https:' in url:
        port = 443
    elif 'http:' in url:
        port = 80

    if port == 443:
        context = create_default_context()
        addr = getaddrinfo(host, port)[0][-1]
        conn = context.wrap_socket(socket(AF_INET), server_hostname=host)
    elif port == 80:
        addr = getaddrinfo(host, port)[0][-1]
        conn = socket()

    conn.connect(addr)
    conn.sendall(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    buf = BytesIO()
    while True:
        data = conn.recv(100)
        if data:
            buf.write(data.text)

            with open(name, 'w') as f:
                f.write(buf)


    conn.close()
        

if __name__ == '__main__':
    URL = 'https://download.dnscrypt.info/dnscrypt-resolvers/json/public-resolvers.json'
    http_get(URL)
