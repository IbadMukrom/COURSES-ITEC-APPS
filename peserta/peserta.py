from django.shortcuts import render, redirect, HttpResponse
from .forms import FormPeserta, ProgramForm, KelasForm, TrainerForm, TambahPendaftaranForm
from .models import Peserta, Program, Pendaftaran, Kelas, Trainer
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic, View
from django.contrib.auth.models import User, Group
from core.lib import useracak
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from core import decorator
from django.views.generic import CreateView, ListView, UpdateView

class PesertaSignUp(View):
    def get(self, request):
        form = FormPeserta
        template_name = 'registration/signupform.html'

        if form.is_valid():
            peserta = form.save(commit=False)
            user = User()
            user.username = useracak()
            user.is_staff = True
            user.set_password(user.username)
            user.save()

            peserta.save = user
            peserta.save()
