from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from users.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dashboard
    path('', login_view),

    path('api/user/', include('users.urls')),
    path('api/accounting/', include('accounting.apis')),

    # All Auth
    path('account/', include('users.urls')),

    path('social-auth/', include('social_django.urls', namespace='social')),

    path('comptabilite/', include('accounting.urls')),

    path('tresorerie/', include('treasury.urls')),
    path('api/treasury/', include('treasury.apis')),

    path('api/billing/', include('billing.apis')),
    path('billing/', include('billing.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
