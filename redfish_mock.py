# redfish_mock.py (обновлённая версия)
from flask import Flask, jsonify, request
import time
import signal
import sys

app = Flask(__name__)
system_state = {"PowerState": "On", "Status": {"State": "Enabled", "Health": "OK"}}

@app.route('/redfish/v1/')
def root():
    return jsonify({"RedfishVersion": "1.18.0", "Systems": {"@odata.id": "/redfish/v1/Systems"}})

@app.route('/redfish/v1/Systems/system')
def system():
    auth = request.authorization
    if not auth or auth.username != 'admin' or auth.password != 'password':
        return jsonify({"error": "Unauthorized"}), 401
    time.sleep(0.02)
    return jsonify(system_state)

def signal_handler(sig, frame):
    print("\nShutting down mock server...")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    app.run(host='0.0.0.0', port=8000, threaded=True)