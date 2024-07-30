from django.urls import path, include

from .views import CreateUsersKycView, KycStatusListView, UsersKycByStatusView, DeleteUsersKycView,\
UpdateUsersKycView, UpdateUsersKycStatusView, UsersKycDetailByUserIdView, UsersKycDetailView

urlpatterns = [
    #Verficacion DNI
    path('kyc/create/one/', CreateUsersKycView.as_view(), name='create_kyc'),
    path('kyc/status/<int:status_id>/', UsersKycByStatusView.as_view(), name='kyc-by-status'),
    path('kyc/delete/one/<str:user_id>/', DeleteUsersKycView.as_view(), name='delete-kyc'),
    path('kyc/update/<str:user_id>/', UpdateUsersKycView.as_view(), name='update-kyc'),
    path('kyc/update/status/<str:user_id>/', UpdateUsersKycStatusView.as_view(), name='update-kyc-status'),
    path('kyc/statuses/', KycStatusListView.as_view(), name='kyc_status_list'),
    # Ruta para obtener la verificación de DNI usando user_id
    path('kyc/user/<str:user_id>/', UsersKycDetailByUserIdView.as_view(), name='users_kyc_by_user_id'),
    # Ruta para obtener la verificación de DNI del usuario autenticado
    path('kyc/detail/', UsersKycDetailView.as_view(), name='users_kyc_detail'),
]