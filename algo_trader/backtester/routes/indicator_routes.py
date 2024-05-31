from flask import Blueprint, jsonify
from lib.indicators import __all__ as indicators_list
from lib.indicators import *

indicator_blueprint = Blueprint('indicator', __name__)

@indicator_blueprint.route('/indicators', methods=['GET'])
def get_indicators():
    indicators_params = []
    for indicator_name in indicators_list:
        indicator_cls = globals()[indicator_name]
        indicators_params.append(indicator_cls.to_dict_class())
    return jsonify(indicators_params)
