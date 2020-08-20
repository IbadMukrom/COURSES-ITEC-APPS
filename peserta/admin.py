from django.contrib import admin
from peserta.models import Peserta, Program, Trainer, Pendaftaran, Kelas


class PesertaAdmin(admin.ModelAdmin):
    # list_display = ['nama', 'program', 'alamat']
    list_display = ('nama_peserta', 'alamat',)
    # list_editable = ['program']

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('nama_program', 'biaya', 'keterangan',)

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('nama_trainer', 'nomor_handphone', 'pendidikan_akhir')

admin.site.register(Peserta, PesertaAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Pendaftaran)
admin.site.register(Kelas)
