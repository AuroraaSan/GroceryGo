from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, ProfileUpdateForm, AddressForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

# Create your views here.
#validation of user 
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    #to prevent user from accessing the register page when logged in
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('shop:product_list')

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save()
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user,
                    phone_number = user_form.cleaned_data['phone_number'],
                    address = user_form.cleaned_data['address'], date_of_birth=user_form.cleaned_data['date_of_birth'])
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

@login_required
def account_view(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        phone_number = profile.phone_number
        address = profile.address
    except Profile.DoesNotExist:
        phone_number = None
        address = None

    context = {
        'user': user,
        'phone_number': phone_number,
        'address': address,
    }

    return render(request, 'account/account_details.html', context)

@login_required
def update_profile(request):
    user = request.user         
    if hasattr(user, 'profile'):
        profile = user.profile
    else:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=profile, user=user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('account')
    else:
        profile_form = ProfileUpdateForm(instance=profile, user=user)

    return render(request, 'account/profile_update.html', {'profile_form': profile_form})

@login_required
def add_address(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.profile = request.user.profile
            new_address.save()
            return redirect('account') 
    else:
        address_form = AddressForm()

    return render(request, 'account/add_address.html', {'address_form': address_form})
