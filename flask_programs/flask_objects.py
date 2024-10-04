import ipaddress, os 

from flask              import Flask, request, abort 
from flask_jwt_extended import JWTManager 

from config.DBInterfacePostgres import DBInterface 
from config.EnvironmentVariables import SECRET_KEY 

def filter_ip_addresses():
    allowed_ip_addresses_list = ipaddress.ip_network("172.21.0.0/16")
    request_client_ip_address = ipaddress.ip_address(request.remote_addr)

    if (request_client_ip_address not in allowed_ip_addresses_list):
        abort(403)

def create_flask_instance():
    flask_db_interface            = Flask(__name__)
    web_token_instance            = JWTManager(flask_db_interface)
    mt2_database_object           = DBInterface()
    flask_db_interface.secret_key = SECRET_KEY 
    flask_db_interface.debug      = True 
    flask_db_interface.before_request(filter_ip_addresses)

    return flask_db_interface, web_token_instance, mt2_database_object 

flask_db_interface, web_token_instance, mt2_database_object = create_flask_instance()
