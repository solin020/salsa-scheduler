
import os 
from starlette.config import Config
dir_path = os.path.dirname(os.path.realpath(__file__))
secret_config = Config("/run/secrets/pythondotenv")
frontend_directory = '/app/salsa-scheduler'
test_prototype_directory = '/app/uploads/test-prototypes'
message_response_directory = '/app/uploads/message-responses'
annotation_directory = '/app/uploads/annotations'
public_url = secret_config('ORIGIN')
account_sid = secret_config('ACCOUNTSID')
auth_token = secret_config('AUTHTOKEN')
test_account_sid = secret_config('TESTACCOUNTSID')
test_auth_token = secret_config('TESTAUTHTOKEN')
db_username = secret_config('DBUSERNAME')
db_password = secret_config('DBPASSWORD')
db_host = secret_config('DBHOST')
db_name = secret_config('DBNAME')
gpg_phassphrase = secret_config('GPGPASSPHRASE')
twilio_number = secret_config('TWILIONUMBER')
test_twilio_number = secret_config('TESTTWILIONUMBER')
