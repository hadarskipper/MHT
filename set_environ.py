import os, sys
import json

secrets_names = ['SA_PASSWORD', 'bot_token']
secrets_json_filename = 'secrets.json'

try:
    with open(secrets_json_filename, 'r') as f:
        secrets_json = json.load(f)
except FileNotFoundError:
    print(f'did not find file {secrets_json_filename}')
    secrets_json = {}

for s in secrets_names:
    print(f'looking for {s} in environment variables')
    s_val = os.environ.get(s)
    
    # check args
    if not s_val:
        print(f'looking for {s} in sys.args')
        arg_key = f'--{s}='
        try:
            arg_idx = [a[:len(arg_key)] for a in sys.argv].index(arg_key)
            s_val = sys.argv[arg_idx][len(arg_key):]
        except ValueError:
            pass
        
    # check secrets in json
    if not s_val:
        print(f'looking for {s} in secrets.json')
        if s in secrets_json.keys():
            s_val = secrets_json[s]
    
    if s_val:
        print(f'setting {s} secret with {len(s_val)*"*"}')
        os.environ[s] = s_val
