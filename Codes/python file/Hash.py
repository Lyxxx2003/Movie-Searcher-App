import hashlib

# Encrypt the usernames
def UserName_Hash(UserName_Sign_p):
    md5 = hashlib.md5()
    md5.update(UserName_Sign_p.encode('utf-8'))
    return md5.hexdigest()

# Encrypt the passwords
def Password_Hash(Password_Sign_p):
    md5 = hashlib.md5()
    md5.update(Password_Sign_p.encode('utf-8'))
    return md5.hexdigest()