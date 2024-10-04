import os, io

import pandas as pd

from flask              import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required 

from werkzeug.security                 import generate_password_hash, check_password_hash
from flask_programs.flask_objects      import flask_db_interface, web_token_instance, mt2_database_object 
from system_programs.encryption_module import retrieve_users_dictionary

@flask_db_interface.route("/login", methods = ["POST"])
def login_to_server():
    username  = request.json.get("username", None)
    password  = request.json.get("password", None)
    user_dict = retrieve_users_dictionary()

    if ((username in user_dict) and (check_password_hash(user_dict[username], password))):
        access_token = create_access_token(identity = username)
        return jsonify(access_token = access_token), 200
    elif ((username in user_dict) and (check_password_hash(user_dict[username], password) is False)):
        return jsonify({"status" : "Bad credentials"}), 401
    elif (username is None or password is None):
        return jsonify({"status" : "Missing login info"}), 400
    
@flask_db_interface.route("/upload_data", methods = ["POST"])
@jwt_required()
def upload_data_to_database():
    table_name  = request.form["table_name"]
    server_name = request.form["server_name"]
    schema_name = request.form["schema_name"]
    upload_data = pd.read_json(io.StringIO(request.files.get("dataframe", None)))

    try:
        mt2_database_object.connection_settings("postgresql", os.getenv("ADMIN_NAME"), os.getenv("ADMIN_PWD"), "localhost", server_name)
        mt2_database_object.upload_to_database(table_name, upload_data, schema_name = schema_name)
        return jsonify({"status" : "Success"}), 200 
    except Exception as E:
        return jsonify({"status" : f"Failure {E}"}), 401

@flask_db_interface.route("/query", methods = ["GET"])
@jwt_required()
def query_database():
    table_name       = request.args.get("server_name")
    server_name      = request.args.get("table_name")
    schema_name      = request.args.get("schema_name")
    columns_list     = request.args.get("column_names").split(",")
    filter_condition = request.args.get("filter_condition", None)
    
    try: 
        mt2_database_object.connection_settings("postgresql", os.getenv("ADMIN_NAME"), os.getenv("ADMIN_PWD"), "localhost", server_name)
        result_json_data = pd.DataFrame(mt2_database_object.get_from_database(table_name, columns_list, filter_condition, schema_name))
        return result_json_data.to_json(), 200
    except Exception as E:
        return jsonify({f"status" : "Operation failure : E"}), 401        
