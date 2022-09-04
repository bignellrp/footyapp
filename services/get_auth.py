# from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash
# from services.lookup import lookup

# auth = HTTPBasicAuth()
# PASSWORD = lookup("httpauth_admin")
# users = {
#     "admin": generate_password_hash(PASSWORD),
# }

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and \
#             check_password_hash(users.get(username), password):
#         return username