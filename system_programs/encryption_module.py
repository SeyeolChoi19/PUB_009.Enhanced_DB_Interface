import os 

import pandas as pd

from cryptography.fernet         import Fernet 
from werkzeug.security           import generate_password_hash, check_password_hash
from config.EnvironmentVariables import KEY_NAME, DB_INTERFACE, TABLE_NAME

def add_users_to_database(username: str, password: str):
    encryption_object = Fernet(os.getenv(KEY_NAME).encode())
    encoded_username  = encryption_object.encrypt(username.encode()).decode()
    encoded_password  = generate_password_hash(password)
    upload_dataframe  = pd.DataFrame({"username" : [encoded_username], "password" : [encoded_password]})
    DB_INTERFACE.upload_to_database(TABLE_NAME, upload_dataframe)
    
def retrieve_users_dictionary():
    encryption_object = Fernet(os.getenv(KEY_NAME).encode())
    result_data_array = DB_INTERFACE.get_from_database(TABLE_NAME, ["*"])
    output_dictionary = {}

    for result in result_data_array:
        output_dictionary[encryption_object.decrypt(result[0].encode()).decode()] = result[1]

    return output_dictionary
