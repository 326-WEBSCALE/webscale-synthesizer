from django.contrib import admin
from .models import ApplicationTable,Snippit,SnippitData,HolesTable,GoogleAuth,Comment
# Register your models here.
admin.site.register(ApplicationTable)
admin.site.register(Snippit)
admin.site.register(SnippitData)
admin.site.register(HolesTable)
admin.site.register(GoogleAuth)
admin.site.register(Comment)
