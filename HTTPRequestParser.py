
def parseRequest(request):
    status = 200
    return status


def getResponse(request):
    status = parseRequest(request)
    response = ''
    http_response = 'HTTP/1.1 {status}\r\n'.format(status=200)
    return response
