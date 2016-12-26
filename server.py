import urllib
from flask import Flask
from flask import request


def readcsv(data):
    """
    Read CSV with header from data string and return a header list
    containing a list of names and also return the list of lists
    containing the data.
    """
    data_lst = data.split('\n')
    headers = data_lst[0].split(',')
    data = []
    for e in data_lst[1:]:
        data.append(e.split(','))
    # remove the space in the end of the file if exist
    if data[len(data)-1] == ['']:
        data.pop()
    return headers, data


def gethistory(ticker):
    """
    Return header list, data (list of lists) for ticker,
    obtained from Yahoo finance.
    """
    link = 'http://ichart.finance.yahoo.com/table.csv?s=' + ticker
    response = urllib.urlopen(link)
    html = response.read()
    return readcsv(html)


def htmltable(headers, data):
    head, body = headers, data
    """Return an HTML table representing the headers and data."""
    htmlhead = '<html>\n<body>\n<table>\n'

    htmlbody_head = '<tr>'
    for word in head:
        htmlbody_head += '<th>' + word + '</th>'
    htmlbody_head += '</tr>'

    htmlbody_body = '\n'
    for lst_item in body:
        htmlbody_body += '<tr>'
        for w in lst_item:
            htmlbody_body += '<td>' + w + '</td>'
        htmlbody_body += '</tr>\n'

    htmlend = '</table>\n</body>\n</html>\n'

    html_str = htmlhead + htmlbody_head + htmlbody_body + htmlend

    return html_str


def jsontable(headers,data):
    head, body = headers, data

    json_head = '{\n  "headers":['
    for i in range(len(head)):
        json_head += '"' + head[i] + '"' + (',' if i < len(head) - 1 else '')
    json_head += '],\n'

    json_body = '  "data":[\n'
    for j in range(len(body)):
        json_body += '    {\n      '
        for i in range(len(head)):
            json_body += '"' + head[i] + '"' + ':' + '"' + body[j][i] + '"' + (',' if i < len(head) - 1 else '')
        json_body += '\n' + '    }' + (',' if j < len(body) - 1 else '') + '\n'

    json_body += '  ]\n}'

    json_str = json_head + json_body

    return json_str


app = Flask(__name__)

# direct input ticker name in url
@app.route("/history/<ticker>")
def history(ticker):
    """
    In response to url /history/ticker, get data from Yahoo finance on
    ticker and return an HTML table representing that data.
    """
    head, body = gethistory(ticker)
    html_str = htmltable(head, body)
    return html_str

# input ticker name in form and redirect to url
@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route("/history", methods=['post'])
def post_history():
    ticker = request.form.get("ticker")
    head, body = gethistory(ticker)
    html_str = htmltable(head, body)
    return html_str

# present the data in json format
@app.route("/data/<ticker>")
def json_history(ticker):
    head, body = gethistory(ticker)
    json_str = jsontable(head, body)
    return json_str

app.run()  # kickstart your flask server

