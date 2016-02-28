import time
import os

types = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/javascript',
    'xml': 'text/xml',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'gif': 'image/gif',
    'png': 'image/png',
    'swf': 'application/x-shockwave-flash'
}


def parseRequest(request, root_dir):
    parsedLine = request.split('\n', 1)[0].split(' ')
    method, url = parsedLine[0], parsedLine[1]

    http_version = 'HTTP/1.1'
    status = '200 OK'
    connection = 'keep-alive'

    if method not in ['GET', 'HEAD']:
        status = '501 Not Implemented'
        connection = 'closed'
    path = url.split('?')[0]
    filename = path.split('\\')[-1]
    type = filename.split('.')[1]
    content_type = 'application/octet-stream'
    try:
        content_type = types[type.lower()]
    except KeyError:
        pass
    file = open(path, 'rb')
    content_length = os.stat(path).st_size
    print(path)

    response = getResponse(http_version, status, date_time_string(), '', content_type, connection, '')
    print(response)
    response = request
    return response


def getResponse(http_version, status, date, server, content_length, content_type, connection, body=None):
    row_end = '\r\n'
    response = http_version + ' ' + status + row_end
    response += 'Date: ' + date + row_end
    response += 'Server: ' + server + row_end
    response += 'Content-Length: ' + content_length + row_end
    response += 'Content-Type: ' + content_type + row_end
    response += 'Connection: ' + connection + row_end
    response += row_end * 2
    if body is not None:
        response += body
    return response


def date_time_string():
    weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    monthname = [None,
                 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    timestamp = time.time()
    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
    s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
        weekdayname[wd],
        day, monthname[month], year,
        hh, mm, ss)
    return s
