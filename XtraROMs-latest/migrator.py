import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XtraROMs.settings')

# Configure Django
django.setup()

from main.models import *
from django.utils.text import slugify
import json

# Load data from JSON file
with open("smartphones.json", "r") as file:
    data = json.load(file)

# Iterate over the data and create/update Device objects
for item in data:
    # Extract name and codename from the current item
    name = item['name']
    codename = item['codename']
    
    # Check if a Device object with the given codename exists
    device, created = Device.objects.get_or_create(codename=codename)
    
    # Update the Device object's modal (corrected from 'modal' to 'model')
    device.name = name
    
    # Save the changes to the Device object
    device.save()

print("Data imported successfully.")