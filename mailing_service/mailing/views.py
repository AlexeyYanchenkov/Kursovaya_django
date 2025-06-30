from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Mailing, Client, MessageLog
from .forms import MailingForm, ClientForm, MessageForm


class ManagerAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Manager").exists()


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(user=user)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailing/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Client.objects.all()
        return Client.objects.filter(mailing__user=user).distinct()


class ClientCreateView(CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]  # укажи нужные поля
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/create_mailing.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Ошибка при валидации формы:", form.errors)
        return super().form_invalid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/edit_mailing.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def test_func(self):
        mailing = self.get_object()
        return mailing.user == self.request.user


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = "mailing/confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def test_func(self):
        mailing = self.get_object()
        return mailing.user == self.request.user


@method_decorator(cache_page(60 * 5), name="dispatch")
class UserStatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "mailing/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        mailings = Mailing.objects.filter(user=user)
        logs = MessageLog.objects.filter(mailing__in=mailings)

        context["total"] = logs.count()
        context["successful"] = logs.filter(status=True).count()
        context["failed"] = logs.filter(status=False).count()
        return context


@method_decorator(login_required, name="dispatch")
class HomeView(View):
    def get(self, request):
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status="started").count()
        unique_clients = Client.objects.count()
        total_logs = MessageLog.objects.count()
        successful_logs = MessageLog.objects.filter(status=True).count()
        failed_logs = MessageLog.objects.filter(status=False).count()

        context = {
            "total_mailings": total_mailings,
            "active_mailings": active_mailings,
            "unique_clients": unique_clients,
            "total_logs": total_logs,
            "successful_logs": successful_logs,
            "failed_logs": failed_logs,
        }

        return render(request, "mailing/home.html", context)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"  # Можно переиспользовать форму создания
    success_url = reverse_lazy("client_form")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")
