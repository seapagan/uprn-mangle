from django.contrib import admin
from .models import Addressbase


class AddressbaseAdmin(admin.ModelAdmin):
    # sort by UPRN by default
    ordering = ["uprn"]
    # display the following fields instead of the __str__
    list_display = ["uprn", "full_address", "postcode", "street_description"]
    # add search fields for UPRN and Address
    search_fields = ["uprn", "full_address"]
    # only 20 rows per page
    list_per_page = 10
    # add the actions on the bottom of screen as well as top
    actions_on_bottom = True

    def has_add_permission(self, request):
        # dont allow adding new AddressBase records from the Admin pages
        return False


admin.site.register(Addressbase, AddressbaseAdmin)
