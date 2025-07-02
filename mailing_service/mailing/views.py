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
        return Client.objects.filter(owner=user)


class ClientCreateView(CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/create_mailing.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get(self, request, *args, **kwargs):
        mailing_form = MailingForm(user=request.user)
        message_form = MessageForm()
        return render(request, self.template_name, {
            'mailing_form': mailing_form,
            'message_form': message_form,
        })

    def post(self, request, *args, **kwargs):
        mailing_form = MailingForm(request.POST, user=request.user)
        message_form = MessageForm(request.POST)

        if mailing_form.is_valid() and message_form.is_valid():
            message = message_form.save(commit=False)
            message.owner = request.user
            message.save()

            mailing = mailing_form.save(commit=False)
            mailing.user = request.user
            mailing.message = message
            mailing.save()
            mailing_form.save_m2m()

            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {
                'mailing_form': mailing_form,
                'message_form': message_form,
            })


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

        # Все рассылки пользователя
        mailings = Mailing.objects.filter(user=user)

        # Уникальные клиенты, связанные с этими рассылками
        clients = Client.objects.filter(mailing__in=mailings).distinct()

        context["total_mailings"] = mailings.count()
        context["active_mailings"] = mailings.filter(status="started").count()
        context["unique_clients"] = clients.count()

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
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("client_form")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")
