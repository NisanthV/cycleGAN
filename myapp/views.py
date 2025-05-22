from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ImageUploadForm, EmailUserCreationForm, EmailAuthenticationForm
from .apps import G_A2B, G_B2A
from PIL import Image
import torch
import torchvision.transforms as transforms
import numpy as np
from io import BytesIO
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .models import UserImage


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = EmailUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            except User.DoesNotExist:
                pass  # Optionally add error message
    else:
        form = EmailAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            return process_image(request, form.cleaned_data)
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def process_image(request, cleaned_data):
    # Get uploaded image and conversion direction
    image_file = cleaned_data['image']
    direction = cleaned_data['direction']

    # Preprocess image
    image = Image.open(image_file).convert('RGB')
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    image_tensor = preprocess(image).unsqueeze(0)

    # Run model inference
    with torch.no_grad():
        if direction == 'A2B':
            output_tensor = G_A2B(image_tensor)
        else:
            output_tensor = G_B2A(image_tensor)

    # Convert output tensor to image
    output_image = tensor_to_image(output_tensor)

    # Prepare response
    buffer = BytesIO()
    output_image.save(buffer, format="PNG")
    response = buffer.getvalue()
    image_file.seek(0)
    # return HttpResponse(response, content_type="image/png")
    original_path = f"users/{request.user.email}/original/{image_file.name}"
    original_image = ContentFile(image_file.read())

    # Save converted image
    converted_buffer = BytesIO()
    output_image.save(converted_buffer, format='PNG')
    converted_image = ContentFile(converted_buffer.getvalue())

    # Create database record
    user_image = UserImage.objects.create(
        user=request.user,
        direction=cleaned_data['direction']
    )
    user_image.original_image.save(original_path, original_image)
    user_image.converted_image.save(
        f"users/{request.user.email}/converted/{image_file.name}",
        converted_image
    )
    user_image.save()

    # Return converted image
    return HttpResponse(converted_buffer.getvalue(), content_type='image/png')

@login_required
def history(request):
    images = UserImage.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'images': images})

def tensor_to_image(tensor):
    """Convert model output tensor to PIL Image"""
    image = tensor.squeeze(0).cpu().numpy()
    image = np.transpose(image, (1, 2, 0))
    image = (image + 1) * 127.5  # Scale from [-1,1] to [0,255]
    image = image.astype(np.uint8)
    return Image.fromarray(image)