import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XtraROMs.settings')

# Configure Django
django.setup()


# load_data.py

import json
from main.models import Credits, Comment, UserProfile, MODLike, Device, CustomROM, CustomMOD, RomComment, ModComment, Blog
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
import markdown
from allauth.account.models import EmailAddress

def convert_to_html(text):
    md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
    processed_text = md.convert(text)
    return processed_text

class Command(BaseCommand):
    help = 'Load data from JSON files into models'

    def handle(self, *args, **options):
        self.load_credits()
        # self.load_users()
        # self.load_custom_roms()
        # self.load_custom_mods()
        # self.load_devices()
        # self.load_comments()
        # self.load_rom_comments()
        # self.load_user_profile()
        # self.load_email()
        # self.load_customrom_devices()

    def load_customrom_devices(self):
        with open('customromdevice.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        for entry in data:
            customrom_id = entry['customrom_id']
            device_id = entry['device_id']

            try:
                # Retrieve the CustomROM instance
                customrom = CustomROM.objects.get(id=customrom_id)
                # Retrieve or create the Device instance
                device, created = Device.objects.get_or_create(id=device_id)
                # Add the device to the custom ROM's many-to-many relationship
                customrom.device.add(device)
            except CustomROM.DoesNotExist:
                # Handle the case when the custom ROM does not exist
                continue

    def load_email(self):
        with open('email.json', 'r', encoding='utf-8') as file:
            users_data = json.load(file)
            for user_data in users_data:
                uploaded_by_id = user_data['user_id']
                try:
                    uploaded_by = User.objects.get(id=uploaded_by_id)
                except User.DoesNotExist:
                    print(f"User with id {uploaded_by_id} does not exist.")
                    continue

                id = user_data['id']
                user_id = uploaded_by
                email = user_data['email']
                verified = user_data['verified']
                primary = user_data['primary']

                EmailAddress.objects.create(id=id, user=user_id, verified = verified, email =email, primary=primary)

    def load_user_profile(self):
        with open('userprofile.json', 'r', encoding='utf-8') as file:
            user_data = json.load(file)
            for u in user_data:
                user_id = u['user_id']
                is_authorized = u['is_authorized']
                profile_picture = u['profile_picture']
                
                # Get the user object based on user_id
                user = get_object_or_404(User, id=user_id)
                
                # Create UserProfile object
                UserProfile.objects.create(
                    id=u['id'],
                    is_authorized=is_authorized,
                    profile_picture=profile_picture,
                    user_id=user_id  # Pass the user's ID, not the User instance
                )
    def load_credits(self):
        with open('credits.json', 'r', encoding = "utf-8") as file:
            credits_data = json.load(file)
            for credit_data in credits_data:
                Credits.objects.create(id=credit_data['id'] ,name=credit_data['name'])
    
    def load_users(self):
        with open('user.json', 'r', encoding='utf-8') as file:
            users_data = json.load(file)
            for user_data in users_data:
                uploaded_by_id = user_data['user_id']
                try:
                    uploaded_by = User.objects.get(id=uploaded_by_id)
                except User.DoesNotExist:
                    print(f"User with id {uploaded_by_id} does not exist.")
                    continue

                user = uploaded_by
                id = user_data['id']
                username = user_data['username']
                email = user_data['email']
                password = user_data['password']
                first_name = user_data['first_name']
                last_name = user_data['last_name']
                
                # Attempt to get the user by username
                user, created = User.objects.get_or_create(id=id)

                # Update user's email, first_name, last_name, and password
                user.username = username
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.set_password(password)
                user.save()


    def load_devices(self):
        with open('devices.json', 'r', encoding = "utf-8") as file:
            devices_data = json.load(file)
            for device_data in devices_data:
                Device.objects.create(
                    id=device_data['id'],
                    name=device_data['name'],
                    codename=device_data['codename']
                )
    
    def load_custom_roms(self):
        with open('custom_roms.json', 'r', encoding='utf-8') as file:
            roms_data = json.load(file)
            for rom_data in roms_data:
                credits_id = rom_data['credits_id']
                credits, _ = Credits.objects.get_or_create(id=credits_id)
                
                uploaded_by_id = rom_data['uploaded_by_id']
                try:
                    uploaded_by = User.objects.get(id=uploaded_by_id)
                except User.DoesNotExist:
                    print(f"User with id {uploaded_by_id} does not exist.")
                    continue
                
                custom_rom = CustomROM.objects.create(
                    id=rom_data['id'],
                    name=rom_data['name'],
                    image=rom_data['image'],
                    android=rom_data['android'],
                    link=rom_data['link'],
                    details=rom_data['details'],
                    credits=credits,
                    uploaded_by=uploaded_by,
                )

    def load_custom_mods(self):
        with open('custom_mods.json', 'r', encoding='utf-8') as file:
            mods_data = json.load(file)
            for mod_data in mods_data:
                credits_id = mod_data['credits_id']
                credits, _ = Credits.objects.get_or_create(id=credits_id)

                uploaded_by_id = mod_data['uploaded_by_id']
                try:
                    if uploaded_by_id:
                        uploaded_by = User.objects.get(id=uploaded_by_id)
                    else:
                        uploaded_by = None
                except User.DoesNotExist:
                    print(f"User with id {uploaded_by_id} does not exist.")
                    continue

                custom_mod = CustomMOD.objects.create(
                    id=mod_data['id'],
                    name=mod_data['name'],
                    image=mod_data['image'],
                    link=mod_data['link'],
                    details=mod_data['details'],
                    credits=credits,
                    uploaded_by=uploaded_by,
                )

    def load_comments(self):
        with open('comments.json', 'r', encoding='utf-8') as file:
            comments_data = json.load(file)
            for comment_data in comments_data:
                uploaded_by_id = comment_data['user_id']
                try:
                    uploaded_by = User.objects.get(id=uploaded_by_id)
                except User.DoesNotExist:
                    print(f"User with id {uploaded_by_id} does not exist.")
                    continue
                Comment.objects.create(
                    id=comment_data['id'],
                    user=uploaded_by,
                    text=comment_data['text'],
                    created_at=comment_data['created_at']
                )

    def load_rom_comments(self):
        with open('rom_comments.json', 'r', encoding='utf-8') as file:
            rom_comments_data = json.load(file)
            for comment_data in rom_comments_data:
                rom_id = comment_data['customrom_id']
                comment_id = comment_data['comment_id']
                try:
                    custom_rom = CustomROM.objects.get(id=rom_id)
                except CustomROM.DoesNotExist:
                    print(f"CustomROM with id {rom_id} does not exist.")
                    continue
                
                try:
                    comment = Comment.objects.get(id=comment_id)
                except Comment.DoesNotExist:
                    print(f"Comment with id {comment_id} does not exist.")
                    continue
                
                RomComment.objects.create(rom=custom_rom, comment=comment)


if __name__ == "__main__":
    Command().handle()
