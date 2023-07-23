from django.shortcuts import render
from main_1.models import PhotoOfWorks, TypeOfServices, ContactOfOrganization, MyObject
from .models import BathRoom, BathRoomType


def renovation_bathroom(request):
    contact_org = ContactOfOrganization.objects.all()
    photo = PhotoOfWorks.objects.all()
    bathroom = BathRoom.objects.all()[:3]
    works = BathRoomType.objects.all()
    context = {
        'bathroom': bathroom,
        'works': works,
        'photo': photo,
        'contact': contact_org,
    }
    return render(request, 'renovation_bathroom/index.html', context)


def gallery(request):
    contact_org = ContactOfOrganization.objects.all()
    bath_images = BathRoom.objects.all()  # получаем поле binding с модели BathRoom, которое имеет связь через ForeignKey
    # с классом PhotoOfWorks и в bathroom_gallery.html выводим фотографии из этого класса
    context = {
        'images': bath_images,
        'contact': contact_org,
    }
    return render(request, 'renovation_bathroom/bathroom_gallery.html', context)


def view_type_objects(request):
    contact_org = ContactOfOrganization.objects.all()
    type_all = TypeOfServices.objects.get(title='Ремонт ванной комнаты')
    print(type_all)
    all_obj = type_all.myobject_set.all()
    print(all_obj)
    context = {
        'all_obj': all_obj,
        'contact': contact_org,
    }
    return render(request, 'repair_of_apartments/info-objects.html', context)