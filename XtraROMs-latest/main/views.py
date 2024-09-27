from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.contrib import messages
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
import mimetypes
import logging

logger = logging.getLogger(__name__)


class HomeView(generic.View):
    template_name = "home.html"
    
    def get(self, request, *args, **kwargs):
        context = {}
        
        roms = CustomROM.objects.all().order_by('-upload_date')[:3]
        context['roms'] = roms
        rom = context.get('roms')
        if rom:
            likes_count_dict = {}
            for rom in roms:
                likes_count = ROMLike.objects.filter(rom=rom).count()
                likes_count_dict[rom.id] = likes_count

            context['likes'] = likes_count_dict
            comment_count_dict = {}
            for rom in roms:
                comment_count = RomComment.objects.filter(rom=rom).count()
                comment_count_dict[rom.id] = comment_count
            
            context['comment'] = comment_count_dict
            context['total_users'] = User.objects.count()
            context['total_items'] = CustomMOD.objects.count() + CustomROM.objects.count()
        
        return render(request, self.template_name, context)

class ManageUserView(generic.ListView, LoginRequiredMixin):

    model = UserProfile
    context_object_name = 'users'
    template_name = 'manage_users.html'
    
    def post(self, request):
        id = request.POST.get("id")
        user = UserProfile.objects.get(id=id)
        if user.is_authorized:
            user.is_authorized = False
            user.save()
            messages.success(request, f"{user.user.username} is unauthorized")
            return JsonResponse({"success": "success"})
        else:
            user.is_authorized =True
            user.save()
            messages.success(request, f"{user.user.username} is authorized")
            return JsonResponse({"success": "success"})

def signup(request):
    return render(request, "account/signup.html")

def createuser(request):
    if request.method == "POST":
        try:
            # Log the request
            logger.debug("Received POST request: %s", request.POST)

            # Get form data
            username = request.POST.get("username")
            firstname = request.POST.get("first_name")
            lastname = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            profile_picture = request.FILES.get("profile_picture")

            # Validate email
            try:
                validate_email(email)
            except ValidationError:
                logger.error("Invalid email address: %s", email)
                return JsonResponse({'status': 'error_400', 'message': 'Invalid email address'}, status=400)

            # Validate username (e.g., no special characters)
            if not re.match("^[A-Za-z0-9_]*$", username):
                logger.error("Invalid username: %s", username)
                return JsonResponse({'status': 'error_400', 'message': 'Username can only contain letters, numbers, and underscores'}, status=400)

            # Validate password (e.g., at least 8 characters, at least one letter and one number)
            if len(password) < 8 or not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
                logger.error("Invalid password")
                return JsonResponse({'status': 'error_400', 'message': 'Password must be at least 8 characters long and contain both letters and numbers'}, status=400)

            # Check if username already exists
            if User.objects.filter(email=email).exists():
                logger.error("Email already in use: %s", username)
                return JsonResponse({'status': 'error_400', 'message': 'Email already in use, try different one!'}, status=400)

            if User.objects.filter(username=username).exists():
                logger.error("Username already taken: %s", username)
                return JsonResponse({'status': 'error_400', 'message': 'Username already taken'}, status=400)
            
            # Validate profile picture file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/webp', 'image/png']
            if profile_picture:
                mime_type, _ = mimetypes.guess_type(profile_picture.name)
                if mime_type not in allowed_types:
                    logger.error("Invalid image format: %s", mime_type)
                    return JsonResponse({'status': 'error_400', 'message': 'Invalid image format. Allowed formats: jpg, jpeg, webp, png'}, status=400)

            # Create and save user
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email)
            user.set_password(password)  # Hash the password
            user.save()

            # Save profile picture
            user_profile = UserProfile.objects.create(user=user)
            if profile_picture:
                user_profile.profile_picture = profile_picture
                user_profile.save()

            logger.debug("User created successfully: %s", username)
            return JsonResponse({'status': 'success', 'message': 'User created successfully'}, status=201)
        except Exception as e:
            logger.error("Error creating user: %s", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        logger.error("Invalid request method")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
def loginuser(request):
    return render(request, "account/login.html")

def login_view(request):
    if request.method == "POST":
        try:
            # Log the request
            logger.debug("Received POST request for login: %s", request.POST)

            # Get form data
            username = request.POST.get("username")
            password = request.POST.get("password")

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logger.debug("User logged in successfully: %s", username)
                return JsonResponse({'status': 'success', 'message': 'Logged in successfully'}, status=200)
            else:
                logger.error("Invalid credentials for username: %s", username)
                return JsonResponse({'status': 'error', 'message': 'Invalid username or password'}, status=400)
        except Exception as e:
            logger.error("Error logging in user: %s", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        logger.error("Invalid request method for login")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
def logout_view(request):
    if request.method == "POST":
        try:
            logout(request)
            logger.debug("User logged out successfully")
            return JsonResponse({'status': 'success', 'message': 'Logged out successfully'}, status=200)
        except Exception as e:
            logger.error("Error logging out user: %s", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        logger.error("Invalid request method for logout")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

class DashboardView(generic.View, LoginRequiredMixin):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        rom_form = UploadROMForm()
        mod_form = UploadMODForm()
        upload_blog = uploadBlogForm()
        user_form = UserProfileForm(instance=user_profile)  # Use instance=user_profile for the user form
        liked_roms = ROMLike.objects.filter(user=request.user)
        liked_mods = MODLike.objects.filter(user=request.user)
        blogs = Blog.objects.filter(written_by=request.user)

        context = {
            "user_profile": user_profile,
            "liked_roms": liked_roms,
            "liked_mods": liked_mods,
            "rom_form": rom_form,
            "mod_form": mod_form,
            "upload_blog": upload_blog,
            "user_form": user_form,
            "blogs": blogs
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_profile = request.user.userprofile
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)  # Instantiate form for POST requests
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('dashboard')  # Redirect to the dashboard page after profile update
        
        # If form is not valid, render the dashboard page with the form
        return render(request, self.template_name, {"user_form": form})
    
class RomsView(generic.ListView):
    template_name = 'roms.html'
    model = CustomROM
    paginate_by = 12
    context_object_name = 'roms'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-upload_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            liked_rom_ids = set(ROMLike.objects.filter(rom__in=context['roms'], user=self.request.user).values_list('rom_id', flat=True))
            context['liked_rom_ids'] = liked_rom_ids
            
        likes_count_dict = {}
        for rom in context['roms']:
            likes_count = ROMLike.objects.filter(rom=rom).count()
            likes_count_dict[rom.id] = likes_count
        context['likes'] = likes_count_dict

        return context
    
    def post(self, request, *args, **kwargs):
        rom_id = request.POST.get("romID")
        if rom_id is not None:
            # Rest of your code...
            rom = get_object_or_404(CustomROM, id=rom_id)
            like, created = ROMLike.objects.get_or_create(user=request.user, rom=rom)

            if not created:
                # If the user already liked it, unlike it
                like.delete()
                return JsonResponse({"status": "unliked"})
            else:
                return JsonResponse({"status": "liked"})
        else:
            return JsonResponse({"status": "error", "message": "'romID' not found in POST data"})

class ROMDetailsView(generic.View):
    template_name = 'rom_details.html'
    context_object_name = 'rom'

    def get(self, request, slug):
        
        rom = get_object_or_404(CustomROM, slug=slug)
        suggested_roms = CustomROM.objects.filter(device__in=rom.device.all())

        formatted_details = mark_safe(
            rom.details.replace("\n", "<br>").replace("-", "&#8226;")
        )
        comments = rom.comments.order_by('-created_at')
        form = CommentForm()
        return render(
            request,
            self.template_name,
            {"rom": rom, "formatted_details": formatted_details, "comments": comments, "form": form, "suggested_roms": suggested_roms},
        )

    def post(self, request, slug):
        rom = get_object_or_404(CustomROM, slug=slug)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            rom.comments.add(comment)
            
            return redirect("rom_details", rom.slug)
        return JsonResponse({"error": "Invalid POST request"})
    
class ModsView(generic.ListView):
    template_name = 'mods.html'
    model = CustomMOD
    context_object_name = 'mods'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-upload_date')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a flag indicating whether the user has liked each mod
        if self.request.user.is_authenticated:
            liked_mod_ids = set(MODLike.objects.filter(mod__in=context['mods'], user=self.request.user).values_list('mod_id', flat=True))
            context['liked_mod_ids'] = liked_mod_ids
            
        # Dictionary to store likes count for each mod
        likes_count_dict = {}
        
        # Calculate likes count for each mod
        for mod in context['mods']:
            likes_count = MODLike.objects.filter(mod=mod).count()
            likes_count_dict[mod.id] = likes_count
        
        context['likes'] = likes_count_dict

        return context
    
    def post(self, request, *args, **kwargs):
        mod_id = request.POST.get("modID")
        if mod_id is not None:
            mod = get_object_or_404(CustomMOD, id=mod_id)
            like, created = MODLike.objects.get_or_create(user=request.user, mod=mod)

            if not created:
                # If the user already liked it, unlike it
                like.delete()
                return JsonResponse({"status": "unliked"})
            else:
                return JsonResponse({"status": "liked"})
        else:
            return JsonResponse({"status": "error", "message": "'modID' not found in POST data"})
        
class MODDetailsView(generic.View):
    template_name = 'mod_details.html'
    context_object_name = 'mod'

    def get(self, request, slug):
        mod = get_object_or_404(CustomMOD, slug=slug)
        suggested_mods = CustomMOD.objects.all()
        suggested_mods = list(suggested_mods)
        random.shuffle(suggested_mods)
        random_mods = random.sample(suggested_mods, 6)
        formatted_details = mark_safe(
            mod.details.replace("\n", "<br>").replace("-", "&#8226;")
        )
        comments = mod.comments.order_by('-created_at')
        form = CommentForm()
        return render(
            request,
            self.template_name,
            {"mod": mod, "formatted_details": formatted_details, "comments": comments, "form": form, "random_mods": random_mods},
        )

    def post(self, request, slug):
        mod = get_object_or_404(CustomMOD, slug=slug)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            mod.comments.add(comment)
            
            return redirect("mod_details", mod.slug)

        return JsonResponse({"error": "Invalid POST request"})
    
class XtraKnowledgeView(generic.ListView):
    template_name = "xtraknowledge.html"
    
    def get(self, request):
        blog = Blog.objects.all()
        upload_blog = uploadBlogForm()
        context = {'blogs': blog, 'upload_blog': upload_blog}
        return render(request, self.template_name, context)
    
    
class DetailsView(generic.View):
    template_name = "details.html"

    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        return render(request, self.template_name, {'blog': blog})
    
class PolicyView(generic.TemplateView):
    template_name = "privacy_policy.html"
    
