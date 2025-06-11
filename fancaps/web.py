"""Wrapper to launch the web interface."""
from importlib import import_module

app = import_module('web.fancaps_web').app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080)
