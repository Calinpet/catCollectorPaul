from django.contrib import admin
from .models import Cat, Feeding, Photo

admin.site.register(Cat)
admin.site.register(Feeding)
admin.site.register(Photo)