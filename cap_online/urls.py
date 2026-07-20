"""
URL configuration for cap_online project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app import views
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from portal import views as portal_views
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
   # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    #path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path("", include("portal.urls")),

    # ──────────────────────────────────────────────────────────
    # RECUPERAR CONTRASEÑA  (EmailJS — sin SMTP)
    # ──────────────────────────────────────────────────────────

    # Paso 1: formulario de email → EmailJS envía el correo
    path(
        "password-reset/",
        portal_views.password_reset_form_view,
        name="password_reset",
    ),

    # Paso 2: página de "revisa tu correo" (informativa)
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    # Paso 3: el usuario llega desde el link del email → pone nueva contraseña
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),

    # Paso 4: contraseña cambiada exitosamente
    path(
        "reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)