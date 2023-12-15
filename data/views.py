from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'base.html', {'section': 'home'})

@login_required
def account_details(request):
    # Your logic here to get the account details
    context = {
        # 'account_detail': account_detail,  # Replace with your actual context variables
    }
    return render(request, 'account/account_details.html', context)

