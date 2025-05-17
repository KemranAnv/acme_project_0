from django.contrib import admin

from .models import Birthday
from .models import Tag

admin.site.register(Birthday)
admin.site.register(Tag)
