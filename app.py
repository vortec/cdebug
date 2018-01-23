from collections import OrderedDict
import socket
import os
from flask import request
from flask import Flask
import json
from flask.ext.redis import Redis



app = Flask(__name__)

app.config['REDIS_HOST'] = 'redis'
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0
redis1 = Redis(app)

def get_environment():
    ret = OrderedDict()
    for key in sorted(os.environ):
        ret[key] = os.environ[key]
    return ret

def get_headers():
    ret = OrderedDict()
    for key in sorted(request.headers):
        key = key[0]
        ret[key] = request.headers[key]
    return ret

def get_cookies():
    ret = OrderedDict()
    for key in sorted(request.cookies):
        ret[key] = request.cookies[key]
    return ret


def dict_to_html_ul(dd, level=0):
    """
    Convert dict to html using ul/li tags
    """
    text = '<ul>\n'
    for k, v in dd.items():
        text += '<li><b>%s</b>: %s</li>\n' % (k, dict_to_html_ul(v, level+1) if isinstance(v, dict) else (json.dumps(v) if isinstance(v, list) else v))
    text += '</ul>'
    return text

def redis_connected(redis):
    try:
        return redis.ping()
    except:
        return False

hostname = socket.gethostname()
environment = dict_to_html_ul(get_environment())


@app.route('/count')
def incr_redis():
    if redis_connected(redis1):
        res = redis1.incr("cdebug-testkey")
        return "Counter increased by host {} to {}".format(hostname, res)
    else:
        return "Not connected to redis"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    counter = 0
    if redis_connected(redis1):
        counter = redis1.get("cdebug-testkey").decode("utf-8")

    output = TEMPLATE.format(hostname=hostname,
                             environment=environment,
                             path=request.path,
                             full_path=request.full_path,
                             headers=dict_to_html_ul(get_headers()),
                             cookies=dict_to_html_ul(get_cookies()),
                             method=request.method,
                             url=request.url,
                             remote_addr=request.remote_addr,
                             redis_connected=redis_connected(redis1),
                             counter=counter)
    return output



TEMPLATE = """
<html>
<body style="font-family: monospace;"">
<h1>Debug</h1>
<h2>Host</h2>
<b>Hostname</b>: {hostname}<br/>
<h3>Environment</h3>
{environment}

<h2>Request</h2>
<b>Path</b>: {path}<br/>
<b>Full path</b>: {full_path}<br/>
<b>Method</b>: {method}<br/>
<b>URL</b>: {url}<br/>
<b>Remote Address</b>: {remote_addr}

<h3>Headers</h3>
{headers}

<h3>Cookies</h3>
{cookies}
<h3>Redis connected?</h3>
{redis_connected}

<p>Redis connections are established to the hostname "redis" on port 6379.</p>

<h3>Redis counter</h3>
{counter}
</body>
</html>
"""


if __name__ == "__main__":
    app.run()
