from django.contrib import admin
from django.urls import path, include
from peserta import views

urlpatterns = [
    path('', views.Dashboard.as_view()),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('input/', views.formInput),
    # path('delete/<int:id>', views.deleteData),

    path('programlist', views.ListProgram.as_view(), name='list-program'),
    path('programnew', views.CreateProgram.as_view(), name='new-program'),
    path('programedit/<int:pk>', views.EditProgram.as_view(), name='edit-program'),
    path('programdelete/<int:id>', views.DeleteProgram.as_view(), name='delete-program'),

    path('pendaftaran', views.CreatePendaftaran.as_view(), name='new-pendaftaran'),

    path('peserta', views.PesertaList.as_view(), name='list-peserta'),

    path('kelas', views.KelasList.as_view(), name='list-kelas'),
    path('kelasnew', views.CreateKelas.as_view(), name='new-kelas'),

    path('trainer', views.TrainerList.as_view(), name='list-trainer'),
    path('trainernew', views.CreateTrainer.as_view(), name='new-trainer'),

    path('tambahpendaftar/<int:id>', views.TambahKePendaftaran.as_view()),
    path('list-pendaftar', views.ListPendaftaran.as_view(), name='list-pendaftar')
]
