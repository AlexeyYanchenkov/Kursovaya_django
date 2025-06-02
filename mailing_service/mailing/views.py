from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserRegistrationForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .models import MessageLog, Mailing
from .forms import MailingForm
from django.contrib.auth.models import Group
from .models import Mailing, Client
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page


@login_required
def mailing_list(request):
    if request.user.groups.filter(name='Manager').exists():
        mailings = Mailing.objects.all()
    else:
        mailings = Mailing.objects.filter(user=request.user)
    return render(request, 'mailing/mailing_list.html', {'mailings': mailings})

@login_required
def client_list(request):
    if request.user.groups.filter(name='Manager').exists():
        clients = Client.objects.all()
    else:
        clients = Client.objects.filter(mailing__user=request.user).distinct()
    return render(request, 'mailing/client_list.html', {'clients': clients})

@login_required
def create_mailing(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)  # Создаём, но не сохраняем
            mailing.user = request.user        # Привязываем пользователя
            mailing.save()                     # Сохраняем в БД
            form.save_m2m()                   # Для ManyToMany полей
            return redirect('home')           # Или другая нужная страница
    else:
        form = MailingForm()
    return render(request, 'mailing/create_mailing.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Важно!
            user.save()
            group = Group.objects.get(name='User')
            user.groups.add(group)

            # Подготовка письма
            current_site = get_current_site(request)
            subject = 'Подтверждение регистрации'
            message = render_to_string('mailing/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return render(request, 'mailing/email_confirmation_sent.html')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'mailing/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'mailing/activation_success.html')
    else:
        return render(request, 'mailing/activation_failed.html')

@cache_page(60 * 5)
@login_required
def user_statistics(request):
    user = request.user
    mailings = Mailing.objects.filter(user=user)
    logs = MessageLog.objects.filter(mailing__in=mailings)

    total = logs.count()
    successful = logs.filter(status=True).count()
    failed = logs.filter(status=False).count()

    context = {
        'total': total,
        'successful': successful,
        'failed': failed,
    }

    return render(request, 'mailing/statistics.html', context)

@login_required
def edit_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    # Проверка прав: только владелец может редактировать
    if mailing.user != request.user:
        raise PermissionDenied("Редактировать можно только свои рассылки.")

    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            return redirect('mailing_list')
    else:
        form = MailingForm(instance=mailing)

    return render(request, 'mailing/edit_mailing.html', {'form': form})

@login_required
def delete_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    # Проверка прав: только владелец может удалять
    if mailing.user != request.user:
        raise PermissionDenied("Удалять можно только свои рассылки.")

    if request.method == 'POST':
        mailing.delete()
        return redirect('mailing_list')

    return render(request, 'mailing/confirm_delete.html', {'mailing': mailing})