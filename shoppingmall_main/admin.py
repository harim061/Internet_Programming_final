from django.contrib import admin
from .models import ShoppingItem,Category,ColorTag,Company,Comment

# Register your models here.

admin.site.register(ShoppingItem)

class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Company,CompanyAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(ColorTag,TagAdmin)
admin.site.register(Comment)