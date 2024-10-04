import string, random, os

from config.DBInterfacePostgres import DBInterface

def generate_random_string():
    components_list = list(string.punctuation) + list(string.ascii_lowercase) + list(string.ascii_uppercase) + [str(i) for i in range(0, 10)]

    return "".join(random.choices(components_list, k = 128))

SECRET_KEY   = generate_random_string()
KEY_NAME     = "MT2_USER_KEY"
SQL_TYPE     = "postgresql"
DB_HOST      = "localhost"
SERVER_NAME  = "MT2_USRS_PWD"
TABLE_NAME   = "MT2_001_OPEN_TABLE"
DB_INTERFACE = DBInterface()
DB_INTERFACE.connection_settings(SQL_TYPE, os.getenv("ADMIN_NAME"), os.getenv("ADMIN_PWD"), DB_HOST, SERVER_NAME)
