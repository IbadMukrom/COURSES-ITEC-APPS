from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import FormPeserta, ProgramForm, KelasForm, TrainerForm, TambahPendaftaranForm
from .models import Peserta, Program, Pendaftaran, Kelas, Trainer
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic, View
from django.contrib.auth.models import User, Group
from core.lib import useracak
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction


class Dashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = 'layout/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['hi'] = "Welcome to my aplication"
        context['peserta'] = Peserta.objects.count()
        context['program'] = Program.objects.count()
        context['pendaftaran'] = Pendaftaran.objects.filter(is_register=True).count()
        context['kelas'] = Kelas.objects.count()
        context['trainer'] = Trainer.objects.count()
    
        return context

class ListProgram(LoginRequiredMixin, generic.ListView):
    model = Program

class FormMixin(object):
    form_class = ProgramForm
    model = Program
    success_url = reverse_lazy('list-program')


class CreateProgram(LoginRequiredMixin, FormMixin, generic.CreateView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["label"] = "Buat Program Baru"

        return context
  

class EditProgram(LoginRequiredMixin, FormMixin, generic.UpdateView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = "Edit Program"

        return context


class DeleteProgram(LoginRequiredMixin, View):
    def get(self, req, *args, **kwargs):
        obj = get_object_or_404(Program, id=kwargs['id'])
        obj.delete()

        return redirect('list-program')


class CreatePendaftaran(LoginRequiredMixin, View):
    def get(self, request):
        form = FormPeserta
        template_name = 'peserta/pendaftaran_form.html'

        return render(request, template_name, {"form": form, "label": "Pendaftaran Baru"})

    @transaction.atomic
    def post(self, request):
        form = FormPeserta(request.POST or None)
        template_name = 'peserta/pendaftaran_form.html'

        if form.is_valid():
            peserta = form.save(commit=False)
            user = User()
            user.username = useracak()
            user.is_staff = True
            user.set_password(user.username)
            user.save()

            peserta.user = user
            peserta.save()

            peserta_group = Group.objects.get_or_create(name='peserta')
            peserta_group[0].user_set.add(user)
            print(peserta_group)

            pendaftaran = Pendaftaran()
            pendaftaran.peserta = peserta
            pendaftaran.program = Program.objects.get(pk=request.POST['program'])
            pendaftaran.save()
            
            return redirect('/peserta')

        return render(request, template_name, {"form": form, "label": "Pendaftaran Baru"})


class PesertaList(LoginRequiredMixin, generic.ListView):
    model = Peserta
    
    def get_queryset(self):
        return self.model.objects.all().order_by('-id')
    
    

class KelasList(LoginRequiredMixin, generic.ListView):
    model = Kelas


class CreateKelas(LoginRequiredMixin, View):

    def get(self, request):
        form = KelasForm
        return render(request, "peserta/kelas_form.html", {"form": form})

    @transaction.atomic
    def post(self, request):
        form = KelasForm(request.POST or None)
        if form.is_valid():
            kelas = form.save()

            trainers = form.cleaned_data.get("trainer")
            pendaftarans = form.cleaned_data.get("pendaftaran")
            kelas.trainer.add(*list(trainers))
            # for t in trainers:
            #     kelas.trainer.add(t)
            
            for p in pendaftarans:
                p.is_register = False
                p.save()
                
                kelas.pendaftaran.add(p)
                print(p)

            return redirect('list-kelas')

        return render(request, "peserta/kelas_form.html", {"form": form})


class TrainerList(LoginRequiredMixin, generic.ListView):
    model = Trainer

class CreateTrainer(LoginRequiredMixin, generic.CreateView):
    form_class = TrainerForm
    model = Trainer
    success_url = reverse_lazy('list-trainer')
    
    @transaction.atomic
    def form_valid(self, form):
        trainer = form.save(commit=False)
        
        userTrainer = User()
        userTrainer.username = useracak()
        userTrainer.is_staff = True
        userTrainer.set_password(userTrainer.username)
        userTrainer.save()
        
        trainer_group = Group.objects.get_or_create(name='trainer')
        trainer_group[0].user_set.add(userTrainer)
        print(trainer_group)

        trainer.user = userTrainer
        trainer.save()
        
        return super(CreateTrainer, self).form_valid(form)


class TambahKePendaftaran(LoginRequiredMixin, View):
    def get(self, request, id):
        data = {
            "peserta": Peserta.objects.get(id=id),
            "form": TambahPendaftaranForm,
        }

        return render(request, "peserta/tambah_ke_pendaftaran.html", data)

    def post(self, request, id):
        peserta = Peserta.objects.get(id=id)
        program = Program.objects.get(id=int(request.POST['program']))
        pendaftaran = Pendaftaran()
        pendaftaran.peserta = peserta
        pendaftaran.program = program
        pendaftaran.keterangan = request.POST['keterangan']
        pendaftaran.save()
        return redirect('list-peserta')

class ListPendaftaran(LoginRequiredMixin, generic.ListView):
    model = Pendaftaran
    template_name = 'peserta/pendaftar_list.html'
    def get_queryset(self):
        return self.model.objects.filter(is_register=True).order_by('-id') 


