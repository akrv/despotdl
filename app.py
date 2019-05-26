from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask import jsonify
from time import sleep
from subprocess import Popen, PIPE, call

import threading

app = Flask(__name__)
Bootstrap(app)

ready = True
output = ""
err = ""


def download_task(playlist, destination):
    global ready, output, err
    ready = False
    p = Popen(['spotdl', '--playlist', playlist], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")

    txt_file = str(err).split(' ')[-1][0:-3]  # txt file to download and delete
    rc = p.returncode
    print(txt_file,output,err)
    # p = Popen(['spotdl', '--list', txt_file, '-f', '/root/Music/'+destination], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # output1, err1 = p.communicate(b"input data that is passed to subprocess' stdin")
    # output += output1
    # err += err1

    call(['spotdl -l ' + txt_file+ ' -f ' + '/root/Music/'+destination], shell=True)

    #call(['rm '+txt_file], shell=True)

    ready = True
    output = ""
    err = ""


@ app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('app.html', ready=ready, output=str(output), err=str(err))


@app.route('/download', methods=['GET', 'POST'])
def start_download():
    if request.method == 'GET':
        return redirect(url_for('index'))
    if request.method == 'POST':
        if ready:
            x = threading.Thread(target=download_task,
                                 args=[request.form.get('playlist'), request.form.get('destination')])
            x.start()
            return render_template('app.html', message='POST')
        else:
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
