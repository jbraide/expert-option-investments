import os, json
from django.core.exceptions import ImproperlyConfigured

with open(os.path.abspath('keys.json')) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except:
        raise ImproperlyConfigured(f'Set the {setting}')