import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.urls import resolve, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError as InvalidError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .forms import LoginForm
from .serializers import UserSerializer
from accounting.models import FiscalYear, Additional, Monitoring


# Create your views here.

def login_view(request):
    login_form = LoginForm()

    if request.user.is_authenticated:
        roles = list()
        for role in request.user.role_set.values():
            roles.append(role['name'])

        if 'Caisse' in roles:
            redirect_url = '/tresorerie/tableau-de-bord'
        else:
            redirect_url = '/comptabilite/'

        next = resolve(request.GET.get('next', redirect_url))
        return redirect(reverse(next.view_name, kwargs=next.kwargs))

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        try:
            year = request.POST['year']
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Nom d'utilisateur et/ou mot de passe sont incorrects!")
            return redirect(reverse('account_login'))
        except MultiValueDictKeyError:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return redirect(reverse('fiscal_year') + '?user_auth=' + user.id.__str__())
            else:
                messages.error(request, "Nom d'utilisateur et/ou mot de passe sont incorrects!")
                return redirect(reverse('account_login'))

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.setdefault('year', year)

            roles = list()
            for role in user.role_set.values():
                roles.append(role['name'])

            if 'Caisse' in roles:
                redirect_url = '/tresorerie/tableau-de-bord'
            else:
                redirect_url = '/comptabilite/'

            next = resolve(request.GET.get('next', redirect_url))
            return redirect(reverse(next.view_name, kwargs=next.kwargs))

    context = {
        'form': login_form
    }
    return render(request, "account/login.html", context)


@api_view(['POST'])
def login_api(request):
    try:
        username = request.data['username']
        password = request.data['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({'message': _("Nom d'utilisateur et/ou mot de passe incorrect!")},
                status=status.HTTP_404_NOT_FOUND)
        user.last_login = datetime.datetime.now(tz=timezone.utc)
        user.save()

        serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        request.session.setdefault('refresh_token', token['refresh'])

        response = Response()
        response.data = {'access_token': token['access'], 'user': serializer.data}
        return response
    except KeyError as e:
        return Response({'message': _(
            "Quelque chose s'est mal passé! Veuillez réessayer ou contacter le fournisseur de ce logiciel")},
                        status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'message': _("Cet utilisateur n'a pas été trouvé!")}, status=status.HTTP_404_NOT_FOUND)


def logout_view(request):
    logout(request)
    return redirect('account_login')


def fiscal_year(request):
    uid = request.GET.get('user_auth')
    user = User.objects.get(id=uid)

    if request.method == 'POST':
        try:
            year = request.POST['year']
            rate = request.POST['rate']
            fiscal_year_add = FiscalYear(year=year, rate=rate)
            fiscal_year_add.save()

            request.session.setdefault('year', str(fiscal_year_add.id))

            roles = list()

            for role in user.role_set.values():
                roles.append(role['name'])

            if 'Caisse' in roles:
                redirect_url = '/tresorerie/tableau-de-bord'
            else:
                redirect_url = '/comptabilite/'

            next = resolve(request.GET.get('next', redirect_url))
            return redirect(reverse(next.view_name, kwargs=next.kwargs))
        except MultiValueDictKeyError:
            messages.error(request, "Le formulaire ne contient pas de clé: year et/ou rate")
            return redirect(reverse('fiscal_year') + '?user_auth=' + user.id.__str__())
        except IntegrityError:
            messages.error(request, "Cette année d'exercice existe déjà")
            return redirect(reverse('fiscal_year') + '?user_auth=' + user.id.__str__())
    context = {
        'user': user
    }
    return render(request, 'fiscal_year.html', context)


@login_required()
def settings(request):
    year_id = request.session.get('year')
    try:
        year = FiscalYear.objects.get(id=year_id)
    except FiscalYear.DoesNotExist:
        return redirect('account_logout')

    additional_accounts = Additional.objects.filter(account_main__account_type__contains='decaissement').all()

    if request.method == 'POST':
        try:
            accounting = request.POST['accounting-id']
            amount = request.POST['warn-amount']
            message = request.POST['message-text']

            if accounting == "":
                for additional_account in additional_accounts:
                    Monitoring(accounting=additional_account, warn_at=amount, year=year, message=message).save()
                messages.success(request, "L'alerte a été ajoutée avec succès")
            else:
                additional_account = Additional.objects.get(id=accounting,
                                                            account_main__account_type__contains='decaissement')
                Monitoring(accounting=additional_account, warn_at=amount, year=year, message=message).save()
                messages.success(request, "L'alerte a été ajoutée avec succès")

            return redirect(reverse('settings'))
        except MultiValueDictKeyError:
            messages.error(request, "Le formulaire ne contient pas de clé: message, et/ou montant, et/ou compte")
            return redirect(reverse('settings'))
        except Additional.DoesNotExist:
            messages.error(request, "Le compte n'existe pas ou n'est pas un compte pour le decaissement")
            return redirect(reverse('settings'))
        except IntegrityError:
            messages.error(request, "Vous avez déjà une alerte pour surveiller le compte choisi")
            return redirect(reverse('settings'))

    context = {
        'additional_accounts': additional_accounts
    }
    return render(request, 'settings.html', context)
