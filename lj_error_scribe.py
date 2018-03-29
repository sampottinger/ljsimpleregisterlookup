import json
import os


import flask
from flask import Markup, request

from ljm_constants import ljmmm


def format_errors(high, low):
    raw_error = zip(ljmmm.get_errors())
    #sort errors based on high and low values
    output_dict = find_error_range_from_errors(low, high, raw_error)
    #send filtered json to tag_summary_template_error.html for rendering
    return flask.render_template("tag_summary_template_error.html", tag =  output_dict)


def find_error_range_from_errors(low, high, raw_error):
	return [x for x in raw_error if x[0]['error'] >= low and x[0]['error'] <= high] 