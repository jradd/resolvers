"Simple=HTTP Methods"
from socket import socket, getaddrinfo, AF_INET
from ssl import create_default_context
import os.path

def http_get(url, overwrite=False):
    """ simple http method get request """
    _, _, host, path = url.split('/', 3)
    filename = url.split('/')[-1]
    if os.path.exists(os.path.abspath(os.path.join(os.path.curdir, filename))):
        if overwrite:
            print('overwriting...\r\n')
            print('--------------------')
            print('\r\n')
        else:
            filename = filename + 'new'
            print('writing to: %s\r\n' % filename)

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
    with open(filename, 'w') as f:
        while True:
            data = conn.recv(100)
            if data:
                f.write(str(bytes(data), 'utf8'))
            else:
                break
    conn.close()

if __name__ == '__main__':
    try:
        import sys.argv
        http_get(sys.argv[1])
    except ImportError:
        http_get('https://www.python.org/')
