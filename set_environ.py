import os, sys
import json

secrets_names = ['SA_PASSWORD', 'bot_token']

try:
    with open('secsdrets.json', 'r') as f:
        secrets_json = json.load(f)
except FileNotFoundError:
    secrets_json = {}

for s in secrets_names:
    s_val = os.environ.get(s)
    
    # check args
    if not s_val:
        arg_key = f'--{s}='
        try:
            arg_idx = [a[:len(arg_key)] for a in sys.argv].index(arg_key)
            s_val = sys.argv[arg_idx][len(arg_key):]
        except ValueError:
            pass
        
    # check secrets in json
    if not s_val:
        if s in secrets_json.keys():
            s_val = secrets_json[s]
    
    if s_val:
        os.environ[s] = s_val
