from django.urls import path, include

from .views import CreateUsersKycView, KycStatusListView, UsersKycByStatusView, DeleteUsersKycView,\
UpdateUsersKycView, UpdateUsersKycStatusView

urlpatterns = [
    #Verficacion DNI
    path('kyc/create/one/', CreateUsersKycView.as_view(), name='create_kyc'),
    path('kyc/status/<int:status_id>/', UsersKycByStatusView.as_view(), name='kyc-by-status'),
    path('kyc/delete/one/<str:user_id>/', DeleteUsersKycView.as_view(), name='delete-kyc'),
    path('kyc/update/<str:user_id>/', UpdateUsersKycView.as_view(), name='update-kyc'),
    path('kyc/update/status/<str:user_id>/', UpdateUsersKycStatusView.as_view(), name='update-kyc-status'),

    #path('kyc/show/one/<int:user_id>/', UsersKycDetailView.as_view(), name='kyc_detail'),
    #path('kyc/edite/one/<int:user_id>/', UsersKycDetailView.as_view(), name='kyc_detail'),
    #path('kyc/delete/one/<int:user_id>/', UsersKycDetailView.as_view(), name='kyc_detail'),
    #EstadosVerificacion
    path('kyc/statuses/', KycStatusListView.as_view(), name='kyc_status_list'),
]