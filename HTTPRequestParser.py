import time
import os
import StringIO
import urllib

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
errors = {
    405: 'Method not allowed',
    404: 'Not Found',
    403: 'Forbidden'
}

error_body = "<h1>Error</h1><br>Highload.Ermakov is as sad as you :("


def parseRequest(request, root_dir):
    parsedLine = request.split('\n', 1)[0].split(' ')
    method, url = parsedLine[0], parsedLine[1]

    http_version = 'HTTP/1.1'
    status = '200 OK'
    connection = 'keep-alive'
    body = None
    content_length = None
    # body = StringIO.StringIO()
    # body.write(error_body)
    # content_length = len(error_body)
    # content_type = 'text/html'
    if method not in ['GET', 'HEAD']:
        body, status, connection, content_type, content_length = setError(405)
        # status = '405 Not Implemented'
        # connection = 'closed'
        return getResponse(http_version, status, date_time_string(), "HighLoad_Ermakov", content_length,
                           content_type, connection, body)

    path = url.split('?')[0]
    path = urllib.unquote(path).decode('utf8')

    if '..' in path:
        body, status, connection, content_type, content_length = setError(404)
        return getResponse(http_version, status, date_time_string(), "HighLoad_Ermakov", content_length,
                           content_type, connection, body)
    # path = path.replace('%20',' ')
    print(root_dir + path)
    filename = path.split('\\')[-1]
    try:
        type = filename.split('.')[-1]
        try:
            content_type = types[type.lower()]
        except KeyError:
            content_type = 'application/octet-stream'
        print(path)
        if os.path.exists(root_dir + path):
            if path[-1] == '/':
                path += 'index.html'
            if os.path.isfile(root_dir + path):
                content_length = os.stat(root_dir + path).st_size
                try:
                    body = open(root_dir + path, 'rb')
                except:
                    pass
            else:
                body, status, connection, content_type, content_length = setError(403)
                # status = '405 Not Implemented'
                # connection = 'closed'
                return getResponse(http_version, status, date_time_string(), "HighLoad_Ermakov", content_length,
                                   content_type, connection, body)
        else:
            body, status, connection, content_type, content_length = setError(404)
            # status = '405 Not Implemented'
            # connection = 'closed'
            return getResponse(http_version, status, date_time_string(), "HighLoad_Ermakov", content_length,
                               content_type, connection, body)
    except:
        body, status, connection, content_type, content_length = setError(404)
        # status = '405 Not Implemented'
        # connection = 'closed'
        return getResponse(http_version, status, date_time_string(), "HighLoad_Ermakov", content_length,
                           content_type, connection, body)

    # print(path)
    if method == 'GET':
        response = getResponse(http_version, status, date_time_string(), "HighLoad_Ermakov", content_length,
                               content_type, connection, body)
    else:
        response = getResponse(http_version, status, date_time_string(), "HighLoad_Ermakov", content_length,
                               content_type, connection)
    # print(response)
    # response = request
    return response


def getResponse(http_version, status, date, server, content_length, content_type, connection, body=None):
    row_end = "\r\n"
    response = http_version + ' ' + status + row_end
    response += 'Date: ' + date + row_end
    response += 'Server: ' + server + row_end
    response += 'Content-Length: ' + str(content_length) + row_end
    response += 'Content-Type: ' + content_type + row_end
    response += 'Connection: ' + connection + row_end
    response += row_end * 1
    return response, body


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


def setError(code):
    body = StringIO.StringIO()
    error_body = "<h1>" + str(code) + ' ' + errors[code] + "</h1><br>Highload.Ermakov is as sad as you :("
    body.write(error_body)
    return body, str(code) + ' ' + errors[code], 'closed', 'text/html', len(error_body)
