from django.contrib import admin

# Register your models here.
from .models import Finch
from .models import Feeding

# Register your models here
admin.site.register(Finch)
admin.site.register(Feeding)
