from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
import markdown

def convert_to_html(text):
    md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
    processed_text = md.convert(text)
    return processed_text

class Credits(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ROMLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rom = models.ForeignKey('CustomROM', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class MODLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mod = models.ForeignKey('CustomMOD', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Device(models.Model):
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.codename})"

class CustomROM(models.Model):
    name = models.CharField(max_length=100)
    android = models.CharField(max_length=10, null=True)
    device = models.ManyToManyField(Device, blank=True, related_name='custom_roms')
    credits = models.ForeignKey(Credits, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to="images")
    link = models.URLField(max_length=225)
    details = models.TextField()
    upload_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(ROMLike, related_name='liked_roms', blank=True)
    comments = models.ManyToManyField(Comment, blank=True, related_name='rom_comments')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_id = uuid.uuid4().hex[:6]  # Generate a unique identifier
            self.slug = f"{base_slug}-{unique_id}"
        self.details = convert_to_html(self.details)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CustomMOD(models.Model):
    name            = models.CharField(max_length=100)
    android         = models.CharField(max_length=10, null=True)
    image           = models.ImageField(upload_to="images")
    credits         = models.ForeignKey(Credits, null=True, on_delete=models.SET_NULL)
    link            = models.URLField()
    details         = models.TextField()
    upload_date     = models.DateField(auto_now=True)
    likes           = models.ManyToManyField(MODLike, related_name='liked_mods')
    comments        = models.ManyToManyField(Comment, blank=True, related_name='mod_comments')
    uploaded_by     = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    slug            = models.SlugField(unique=True, blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_id = uuid.uuid4().hex[:6]  # Generate a unique identifier
            self.slug = f"{base_slug}-{unique_id}"
        self.details = convert_to_html(self.details)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_authorized = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="profile_picture/", null=True, blank=True, default="profile_pictures/akatsuki_logo_xwqj26.png")

    def __str__(self):
        return self.user.username

class RomComment(models.Model):
    rom = models.ForeignKey(CustomROM, on_delete=models.CASCADE, related_name='rom_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class ModComment(models.Model):
    mod = models.ForeignKey(CustomMOD, on_delete=models.CASCADE, related_name='mod_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class Blog(models.Model):
    title = models.CharField(max_length=225)
    tag = models.CharField(max_length=20)
    description = models.TextField()
    written_by = models.ForeignKey(User, null= True, blank=True , on_delete=models.CASCADE)
    date = models.DateField(auto_now = True)
    slug = models.SlugField(unique=True, blank=True, null=True, default=None)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify("blog")
            unique_id = uuid.uuid4().hex[:6]
            self.slug = f"{base_slug}-{unique_id}"
        self.description = convert_to_html(self.description)
        super().save(*args, **kwargs)