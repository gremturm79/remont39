from django.contrib import admin
from .models import PhotoOfWorks, TypeOfServices, CalculateTableEx, ListOfWorks, \
    ContactOfOrganization, ProfileUser, Review, Company, SummOfWorks, PricingAndSummWorks, ApartmentPrice, \
    ImageFavorite, MyObject, LocationObjects


@admin.register(PricingAndSummWorks)
class PricingAndSummWorksAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'estimate', 'date')
    search_fields = ['owner', 'date']
    list_filter = ['owner', 'estimate', 'date']


admin.site.register(PhotoOfWorks)
admin.site.register(TypeOfServices)
admin.site.register(CalculateTableEx)
admin.site.register(ListOfWorks)
admin.site.register(ContactOfOrganization)
admin.site.register(ProfileUser)
admin.site.register(Review)
admin.site.register(Company)
admin.site.register(SummOfWorks)
# admin.site.register(PricingAndSummWorks)
admin.site.register(ApartmentPrice)
admin.site.register(ImageFavorite)
admin.site.register(MyObject)
admin.site.register(LocationObjects)
