from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import re
import models
from werkzeug.exceptions import HTTPException
from random import randint
import time

import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import numpy as np
import geopandas as gpd
import pickle
import joblib

import fraud_handler as fh
import credit_handler as ch

app = Flask(__name__)

base_path = "/project/"

@app.route("/risk_engine", methods=["POST"])
def risk_engine():
    start_time = time.time()
    data = request.get_json()
    
    mod_apps_filepath = '/project/data/mod_apps_list.csv'
    daily_apps_filepath = '/project/data/daily_apps_list.csv'
    indonesia_isp_filepath = 'project/data/indonesia_isp.csv'
    fraud_model_version = '1.0'
    fraud_model_date_deployed = '2021-08-04'
    
    
    fraud_checks = fh.FraudHandler(data, mod_apps_filepath, daily_apps_filepath, indonesia_isp_filepath)
    
    result = {
        "message": "SUCCESS",
        "userid": data['user']['_id'],
        "process_time": time.time() - start_time,
        "timestamp": str(datetime.now()),
        "fraud_result": {
            "version": fraud_model_version,
            "build_version": build_version,
            "score": credit_score,
            "log_score": np.log(credit_score),
            "model": model_algorithm,
            "credit_decision": credit_decision,
            "credit_decision_notes": credit_decision_notes,
            "credit_quality": credit_quality,
            "credit_limit": credit_limit
        }
    }
        
    return str(result).replace("'", '"')

