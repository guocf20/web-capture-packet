import subprocess
import os
import time
from flask import Flask, render_template, request, send_from_directory,jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'captures/'

tcpdump_process = None
capture_filename = None

@app.route('/')
def index():
    print("in index")
    return render_template('index.html')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    global tcpdump_process, capture_filename
    print("starting capture......")
    ip = request.form['ip']
    port = request.form['port']
    duration = request.form['duration']

    capture_filename = 'capture_{}.pcap'.format(int(time.time()))
    tcpdump_command = 'tcpdump -i any -w {}{} host {} and port {} -G {} -W 1'.format(app.config['UPLOAD_FOLDER'],capture_filename, ip, port, duration)

    tcpdump_process = subprocess.Popen(tcpdump_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    response = {'status': 'success' , 'name': capture_filename, 'duration': duration}
    return jsonify(response)

@app.route('/stop_capture', methods=['GET'])
def stop_capture():
    global tcpdump_process, capture_filename
    print("stopping capture...")
    if tcpdump_process is not None:
        tcpdump_process.terminate()
        tcpdump_process = None

        response = {'status': 'success' , 'name': capture_filename}
        return jsonify(response)

    
    response = {'status': 'success' , 'name': "null"}
    return jsonify(response)

@app.route('/download_capture', methods=['GET'])
def download_capture():
    global capture_filename
    print(capture_filename)
    if capture_filename is not None:
        return send_from_directory(app.config['UPLOAD_FOLDER'], capture_filename, as_attachment=True)

    return 'No capture file available'

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(host='0.0.0.0')

