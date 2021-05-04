import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests


# Use this fixture to get the URL of the server.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "simple.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

def test_add(url):
    requests.post(f"{url}/name/add", data={ 'name' : 'Asus' })
    requests.post(f"{url}/name/add", data={ 'name' : 'Acer' })
    requests.post(f"{url}/name/add", data={ 'name' : 'Dell' })
    payload = requests.get(f"{url}/names").json()
    assert payload['names'] == [ 'Asus', 'Acer', 'Dell' ]

def test_remove(url):
    requests.post(f"{url}/name/add", data={ 'name' : 'Asus' })
    requests.post(f"{url}/name/add", data={ 'name' : 'Acer' })
    requests.delete(f"{url}/name/remove", data={ 'name' : 'Acer' })
    payload = requests.get(f"{url}/names").json()
    assert payload['names'] == [ 'Asus' ]
