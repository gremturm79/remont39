from django.shortcuts import render
from .models import Apartments, ApartmentType
from main_1.models import PhotoOfWorks, ContactOfOrganization, TypeOfServices, MyObject


def repair_of_apartments(request):
    contact_org = ContactOfOrganization.objects.all()
    apartment = Apartments.objects.all()[0:3]
    works = ApartmentType.objects.all()
    context = {
        'apartment': apartment,
        'works': works,
        'contact': contact_org,
    }
    return render(request, 'repair_of_apartments/index.html', context)


def apartment_gallery(request):
    contact_org = ContactOfOrganization.objects.all()
    apartment_photo = Apartments.objects.all()
    context = {
        'images': apartment_photo,
        'contact': contact_org,
    }
    return render(request, 'repair_of_apartments/apartment_gallery.html', context)


def view_type_objects(request):
    contact_org = ContactOfOrganization.objects.all()
    type_all = TypeOfServices.objects.get(title='Ремонт квартир')
    all_obj = type_all.myobject_set.all()
    # all_obj = type_all.myobject_set.all()
    print(all_obj)
    context = {
        'all_obj': all_obj,
        'contact': contact_org,
    }
    return render(request, 'repair_of_apartments/info-objects.html', context)
