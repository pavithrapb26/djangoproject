from django.urls import path
from . import views

urlpatterns=[
    path('',views.home1,name='home'),
    path('userpage/',views.userpage,name='userpage'),
    path('login/',views.user_login,name='login'),
    path('welcome/',views.welcome,name='welcome'),
    path('register/',views.user_register,name='register'),
    path('medicines/',views.medicine_list,name='medicine_list'),
    path('medicines/<int:medicine_id>/',views.medicine_detail,name='medicine_detail'),
    path('buy_medicine/', views.buy_medicine, name='buy_medicine'),
    path('view_invoice/', views.view_invoice, name='view_invoice'),
    path('prescriptions/', views.manage_prescriptions, name='manage_prescriptions'),
    path('prescriptions/create/', views.create_prescription, name='create_prescription'),
    path('prescription_success/<int:prescription_id>/',views.prescription_success, name='prescription_success'),
    path('sales_details/',views.sales_details, name='sales_details'),
    path('medicine-stock/',views.medicine_stock_availability, name='medicine_stock_availability'),
    path('search-medicines/', views.search_medicines, name='search_medicines'),
    path('recent-purchases/',views.recent_purchases, name='recent_purchases'),
    path('profile-management/',views.profile_management, name='profile_management'),
    path('happy-customers/', views.happy_customers, name='happy_customers'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('about/',views.about_page, name='about'),

]







#    path('upload-prescription/', views.upload_prescription,name='upload_prescription'),
#     path('prescriptions/', views.prescription_list, name='prescription_list'),
#     path('purchase-medicine/<int:prescription_id>/', views.purchase_medicine, name='purchase_medicine'),










#     path('accounts/login/',views.loginview,name='login'),
#     path('logout',views.logout_view,name="logout"),
#     path('accounts/sign_up/',views.sign_up,name="signup"),
#     path('reset',views.resethome,name='reset'),
#     path('passwordreset',views.resetpassword,name="passwordreset"),

