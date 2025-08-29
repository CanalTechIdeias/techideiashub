from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse

from .models import Profile
from .forms import CustomUserCreationForm, ProfileUpdateForm

def sign_up(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/sign_up.html", {"form": form})

# View for public profile by slug
def public_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    is_owner = request.user.is_authenticated and request.user == profile.user
    return render(request, "users/profile.html", {"profile": profile, "is_owner": is_owner})

# View for updating profile
@login_required
def update_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug, user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect(reverse("public_profile", args=[profile.slug]))
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, "users/profile_update.html", {"form": form, "profile": profile})

# View for deleting profile
@login_required
def delete_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug, user=request.user)
    if request.method == "POST":
        user = profile.user
        profile.delete()
        user.delete()
        messages.success(request, "Perfil deletado com sucesso!")
        return redirect("home")
    return render(request, "users/profile_delete.html", {"profile": profile})
