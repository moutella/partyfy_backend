import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partyfy_backend.settings")
django.setup()

# Location domains and initial data
call_command('loaddata', 'adjective', app_label='party_mode')
call_command('loaddata', 'animal', app_label='party_mode')