"""
Hello API route handlers

"""
from flask import jsonify,render_template
import datetime
from . import api


@api.route('/hello/')
def hellow():
    #return jsonify(dict(hello=name))
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]
    #result = _get_ocr_tokens("http://ec2-18-206-38-255.compute-1.amazonaws.com/ocr_images/bill1.jpeg")
    return render_template('index.html', times=dummy_times)


