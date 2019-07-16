from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# region User registration form
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully. Now you can login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
# endregion

# region UserInformation not in use just for testing
# def user_information(request):
#     if request.method == 'POST':
#         user_info_form = UserInformation(request.POST)
#         if user_info_form.is_valid():
#             user_info_username = user_info_form.cleaned_data.get('name')
#             messages.success(request, f'Details are saved {user_info_username} !')
#             return redirect('blog-home')
#     else:
#         user_info_form = UserInformation()
#     return render(request, 'users/userinfo.html', {'user_info_form': user_info_form})
# endregion

# region User profile form
@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your account has been updated ')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }

    return render(request, 'users/profile.html', context)
# endregion
