import secrets
import os

def save_prof(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    raw_fn = random_hex + f_ext
    return raw_fn