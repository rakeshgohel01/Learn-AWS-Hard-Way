import hmac
import hashlib
import base64

def calculate_secret_hash(username, client_id, client_secret):
    message = username + client_id
    dig = hmac.new(client_secret.encode('utf-8'),
                   msg=message.encode('utf-8'),
                   digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

username = 'test2'
client_id = '1nau172bra5rkpejavfj2ruvv3'
client_secret = '1bta25crkldftvqfuc40bc1kv48vtlfjs476a5kbh47nmvsptu8b'

secret_hash = calculate_secret_hash(username, client_id, client_secret)
print(secret_hash)
