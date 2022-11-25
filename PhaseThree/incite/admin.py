from django.contrib import admin
from .models import *
# Register your models here.

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'default'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        print("Saving...")
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        print("Deleting...")
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        print("Querying...")
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        print("formfieldfk...")
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        print("formfieldmany2many")
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

admin.site.register(User, MultiDBModelAdmin)
admin.site.register(Customer, MultiDBModelAdmin)
admin.site.register(Seller, MultiDBModelAdmin)
admin.site.register(Product, MultiDBModelAdmin)
admin.site.register(Order_item, MultiDBModelAdmin)
admin.site.register(Order, MultiDBModelAdmin)
admin.site.register(Cart, MultiDBModelAdmin)
admin.site.register(Checkout, MultiDBModelAdmin)
