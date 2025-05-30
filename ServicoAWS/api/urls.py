"""
URL configuration for ServicoAWS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import ConfirmarPagamentoFinalView, ConfirmarRecolhaView, FaceRegisterView, FaceLoginView, CreateRepairRequestView, RepairStatusView, ShopInfoView, ClientApprovalView, StaffConcluiReparacaoView, StaffConfirmarPresencaView, AppointmentsListView, AllRepairsView, AllUsersView,UserAppointmentsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('face-register/', FaceRegisterView.as_view()),
    path('face-login/', FaceLoginView.as_view()),
    path('repair-request/', CreateRepairRequestView.as_view()),
    path('repair-status/', RepairStatusView.as_view()),
    path('shop-info/', ShopInfoView.as_view()),
    path('client-approval/', ClientApprovalView.as_view()),
    path('client-present/', StaffConfirmarPresencaView.as_view()),
    path('repair-done/', StaffConcluiReparacaoView.as_view()),
    path('client-pay/', ConfirmarPagamentoFinalView.as_view()),
    path('confirmar-recolha/', ConfirmarRecolhaView.as_view()),
    path('all-appointments/', AppointmentsListView.as_view()),
    path('all-repairs/', AllRepairsView.as_view()),
    path('all-users/', AllUsersView.as_view()),
    path('user-appointments/', UserAppointmentsView.as_view()),
]

