from .models import CustomROM, CustomMOD
from django.db.models import Q
from django.http import JsonResponse
from .forms import *
from django.shortcuts import redirect, get_object_or_404, render
import logging
from django.contrib import messages


logger = logging.getLogger(__name__)

def search_roms(request):
    query = request.GET.get("q", "")
    if query:
        filtered_roms = CustomROM.objects.filter(
            Q(name__icontains=query)
            | Q(device__name__icontains=query)
            | Q(device__codename__icontains=query)
        )

        roms_data = []
        for rom in filtered_roms:
            likes_count = rom.likes.count()
            comments_count = rom.comments.count()
            rom_data = {
                "id": rom.id,
                "name": rom.name,
                "android": rom.android,
                "devices": [{"name": device.name, "codename": device.codename} for device in rom.device.all()],
                "details": rom.details,
                "link": rom.link,
                "upload_date": rom.upload_date,
                "image_url": rom.image.url,
                "likes": likes_count,
                "credits": rom.credits.name if rom.credits else None,
                "slug": rom.slug,
                "is_staff": request.user.is_staff,
                "is_authenticated": request.user.is_authenticated,
            }
            roms_data.append(rom_data)
    else:
        roms_data = []

    return JsonResponse({"results": roms_data})

def search_mods(request):
    query = request.GET.get("q", "")
    if query:
        filtered_mods = CustomMOD.objects.filter(
            Q(name__icontains=query)
        )

        mods_data = []
        for mod in filtered_mods:
            likes_count = mod.likes.count()
            mod_data = {
                "id": mod.id,
                "name": mod.name,
                "details": mod.details,
                "link": mod.link,
                "upload_date": mod.upload_date,
                "image_url": mod.image.url,
                "likes": likes_count,
                "credits": mod.credits.name if mod.credits else None,
                "slug": mod.slug,
                "is_staff": request.user.is_staff,
                "is_authenticated": request.user.is_authenticated,
            }
            mods_data.append(mod_data)
    else:
        mods_data = []

    return JsonResponse({"results": mods_data})


def edit_rom(request, slug):
    rom = get_object_or_404(CustomROM, slug=slug)

    if request.method == "POST":
        edit_form = EditROMForm(request.POST, request.FILES, instance=rom)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, f'{rom.name} modified successfully')
            return redirect("roms") 
    else:
        # Ensure that the credits field of the CustomROM instance is an instance of Credits
        # You can do this by fetching the Credits instance associated with the CustomROM instance
        # or passing None if there's no associated Credits instance
        initial_credits = rom.credits if rom.credits else None
        edit_form = EditROMForm(instance=rom, initial={'credits': initial_credits})

    context = {"edit_form": edit_form, "rom": rom}
    return render(request, "edit_rom.html", context)


def edit_mod(request, slug):
    mod = get_object_or_404(CustomMOD, slug=slug)

    if request.method == "POST":
        edit_form = EditMODForm(request.POST, request.FILES, instance=mod)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, f'{mod.name} modified successfully')
            return redirect("mods") 
    else:
        # Ensure that the credits field of the CustomROM instance is an instance of Credits
        # You can do this by fetching the Credits instance associated with the CustomROM instance
        # or passing None if there's no associated Credits instance
        initial_credits = mod.credits if mod.credits else None
        edit_form = EditMODForm(instance=mod, initial={'credits': initial_credits})

    context = {"edit_form": edit_form, "rom": mod}
    return render(request, "edit_rom.html", context)

def upload_roms(request):
    try:
        if request.method == 'POST':
            form = UploadROMForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_rom = form.save()
                messages.success(request, f'{uploaded_rom.name} uploaded successfully')
                return redirect('roms')  # Redirect to a success URL after saving
            else:
                # Form is not valid, display error message
                error_message = "An error occurred while uploading. Please check the form and try again."
                messages.error(request, error_message)
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"An error occurred: {e}")

    # If an error occurs or form is invalid, render the form again
    form = UploadROMForm()
    return render(request, 'dashboard.html', {'form': form})

def upload_mods(request):
    try:
        if request.method == 'POST':
            form = UploadMODForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_mod = form.save()
                messages.success(request, f'{uploaded_mod.name} uploaded successfully')
                return redirect('mods')  # Redirect to a success URL after saving
            else:
                # Form is not valid, display error message
                error_message = "An error occurred while uploading. Please check the form and try again."
                messages.error(request, error_message)
                
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"An error occurred: {e}")
        
    form = UploadMODForm()
    return render(request, 'dashboard.html', {'form': form})


def edit_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if request.method == "POST":
        edit_form = BlogEditForm(request.POST, instance=blog)
        if edit_form.is_valid():
            edit_form.written_by = request.user
            edit_form.save()
            messages.success(request, f'Blog modified successfully')
            return redirect("xtraknowledge", slug) 
    else:
        edit_form = BlogEditForm(instance=blog)

    context = {"edit_form": edit_form, "blog": blog}
    return render(request, "edit_details.html", context)