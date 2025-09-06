from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    
]


