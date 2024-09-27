import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "XtraROMs.settings")

# Configure Django
django.setup()

from main.models import Blog, UserProfile
import requests
import json


def second():
    blogs = Blog.objects.all()

    for blog in blogs:
        text = requests.get(
            "https://best-project-ashy.vercel.app/api/markdown/",
            {"text": blog.description},
        )
        processed_text = text.json().get("processed_text")
        blog.description = processed_text
        blog.save()


def first():
    with open("out.json", "r") as file:
        data = json.load(file)

        for item in data:
            blog = Blog(
                id=item["id"],
                title=item["title"],
                description=item["description"],
                date=item["date"],
                link=item["link"],
                written_by=item["written_by"],
            )
            blog.save


def third():
    user = UserProfile.objects.all()

    for pfp in user:
        if pfp.profile_picture == None:
            pfp.profile_picture == "C:/Users/siddh/OneDrive/Desktop/XtraROMs/main/static/images/akatsuki_logo.png"
        pfp.save


def fourth():
    text = requests.get(
        "https://best-project-ashy.vercel.app/api/markdown/",
        params={
            "text": """Flashing a custom ROM on an Android device involves several steps, and it's crucial to follow them carefully to avoid damaging your device or losing data. Below is a step-by-step guide to flashing a custom ROM generally:

1. **Backup your data**: Before proceeding with any modifications, it's essential to backup all your data, including contacts, messages, photos, videos, and any other important files. This ensures that you can restore your data if something goes wrong during the flashing process.

2. **Unlock bootloader**: Most Android devices come with locked bootloaders by default. You'll need to unlock the bootloader to install a custom ROM. Unlocking the bootloader varies depending on the manufacturer and device model. You can usually find instructions on the manufacturer's website or XDA Developers forum.

3. **Install a custom recovery**: A custom recovery, such as TWRP (Team Win Recovery Project) or ClockworkMod Recovery, is required to flash custom ROMs. You can install a custom recovery using fastboot or by flashing it through the bootloader. Make sure to download the correct recovery image for your device.

4. **Download the custom ROM**: Choose a custom ROM that is compatible with your device. It's essential to select a ROM from a reputable source, such as XDA Developers, where you can find ROMs tailored to specific devices. Download the ROM zip file and any additional files, such as Google Apps (GApps), if needed.

5. **Transfer ROM to device**: Once you've downloaded the custom ROM and any necessary files, transfer them to your device's internal storage or external SD card. Connect your device to your computer using a USB cable and transfer the files directly, or use a file manager app on your device to download the files.

6. **Enter recovery mode**: Power off your device completely. Then, boot into recovery mode by pressing and holding the appropriate key combination. This combination varies depending on the device but typically involves pressing the power button and volume down button simultaneously until the device boots into recovery mode.

7. **Backup current ROM (optional)**: Before flashing the custom ROM, it's a good idea to create a backup of your current ROM using the custom recovery. This backup, often referred to as a NANDroid backup, allows you to restore your device to its previous state if something goes wrong during the flashing process.

8. **Wipe data and cache**: In the custom recovery, perform a factory reset or wipe data/factory reset to clear your device's internal storage and cache partitions. This step ensures a clean slate for installing the new ROM and prevents conflicts with the existing system.

9. **Flash the custom ROM**: Navigate to the "Install" or "Install ZIP" option in the custom recovery and select the custom ROM zip file you transferred earlier. Confirm the flashing process and wait for it to complete. If you downloaded additional files, such as GApps, flash them in the same way after flashing the ROM.

10. **Reboot your device**: Once the flashing process is complete, reboot your device from the recovery menu. Your device should now boot into the newly installed custom ROM. The first boot may take longer than usual as the system initializes.

11. **Setup and customization**: Follow the on-screen instructions to set up your device and customize it according to your preferences. You can configure settings, install additional apps, and personalize the user interface to your liking.

12. **Test and troubleshoot**: After installing the custom ROM, thoroughly test your device to ensure everything is working correctly. Check for any issues with hardware functionality, network connectivity, and app compatibility. If you encounter any problems, refer to the ROM's forum thread or community for assistance.

13. **Enjoy your custom ROM**: Once you've verified that the custom ROM is stable and meets your needs, you can enjoy the benefits of enhanced performance, customization options, and additional features not available in the stock ROM.

It's essential to note that flashing a custom ROM voids the device's warranty and carries some risks, including the potential for data loss, bricking the device, or security vulnerabilities. Therefore, it's essential to research thoroughly, follow instructions carefully, and proceed with caution when flashing custom ROMs."""
        },
    )
    processed_text = text.json().get("processed_text")
    print(processed_text)
    
fourth()