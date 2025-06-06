from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.contrib import admin
from django.urls import include, path, reverse_lazy

from django.conf import settings

from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
        ),
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('birthday/', include('birthday.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.page_not_found'
