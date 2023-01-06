from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.urls import resolve, reverse

from .forms import LoginForm


# Create your views here.

def login_view(request):
    login_form = LoginForm()

    if request.user.is_authenticated:
        return redirect('accounting_plan_index')

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        year = request.POST['year']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print('Utilisateur pas trouvé')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.setdefault('year', year)

            roles = list()
            for role in user.role_set.values():
                roles.append(role['name'])

            if 'Caisse' in roles:
                redirect_url = '/tresorerie/cdf/depenses/'
            else:
                redirect_url = '/plan-comptable/'

            next = resolve(request.GET.get('next', redirect_url))
            return redirect(reverse(next.view_name, kwargs=next.kwargs))

    context = {
        'form': login_form
    }
    return render(request, "account/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('account_login')
