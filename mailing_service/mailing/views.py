from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page

from .models import Mailing, Client, MessageLog
from .forms import MailingForm

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
            mailing = form.save(commit=False)
            mailing.user = request.user
            mailing.save()
            form.save_m2m()
            return redirect('mailing_list')
    else:
        form = MailingForm()
    return render(request, 'mailing/create_mailing.html', {'form': form})

@login_required
def edit_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

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

    if mailing.user != request.user:
        raise PermissionDenied("Удалять можно только свои рассылки.")

    if request.method == 'POST':
        mailing.delete()
        return redirect('mailing_list')

    return render(request, 'mailing/confirm_delete.html', {'mailing': mailing})

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