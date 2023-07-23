from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from .models import PhotoOfWorks, TypeOfServices, ListOfWorks, ContactOfOrganization, \
    Review, Company, SummOfWorks, PricingAndSummWorks, ApartmentPrice, ImageFavorite, LocationObjects, MyObject
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ContactForm, UserForm
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import ListOfWorksForm, SendMessageForm, ProfileUserForm, ReviewForm, ApartmentPriceForm, MyObjectForm
from django.contrib import messages
from .utils import send_message, personal_view, cost_works, search_reviews, paginate_reviews, cost_works_apartments, \
    add_image, check_city
from forum.models import Thread, Category
from forum.forms import ThreadForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from bing_image_downloader.downloader import download
from transliterate import translit
import io
import datetime
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.units import inch
import reportlab
import os


def index(request):
    # print(request.build_absolute_uri()) получение URL
    if request.method == 'POST':
        location_all_city = LocationObjects.objects.values_list('city', flat=True)  # список локаций
        # print(location_all_city)
        # location_href = LocationObjects.location_city(request, *location_all_city)
        # location = LocationObjects.objects.get(city='Светлогорск').bind.all()
        # print(location_href)
        location = LocationObjects.objects.all()
        category = Category.objects.all()
        binding = Thread.objects.all()
        contact_org = ContactOfOrganization.objects.all()
        company = Company.objects.all()
        company_services = Company.objects.get(id=1)
        company_all = company_services.typeofservices_set.all()
        color = 'radial-gradient(#8cc2cc, transparent)'
        context = {
            'company': company,
            'company_all': company_all,
            'contact': contact_org,
            'forum': category,
            'bind': binding,
            'color': color,
            'location': location,
            'location_href': location_all_city
        }

        if request.user.is_authenticated:
            message = request.POST['phone']
            message_text = 'Вас просят перезвонить по номеру ' + '\n' + '+7-' + message
            send_message(message_text)
            return render(request, 'main/index.html', context)
        # else:
        # messages.info(request, 'Необходимо зарегистрироваться')
        # return redirect('enter')
    location_all_city = LocationObjects.objects.values_list('city', flat=True)  # список локаций
    location = LocationObjects.objects.all()
    category = Category.objects.all()
    binding = Thread.objects.all()
    contact_org = ContactOfOrganization.objects.all()
    company = Company.objects.all()
    company_services = Company.objects.get(id=1)
    company_all = company_services.typeofservices_set.all()
    color = 'radial-gradient(#8cc2cc, transparent)'  # выделение раздела нахождения в меню
    context = {
        'company': company,
        'company_all': company_all,
        'contact': contact_org,
        'forum': category,
        'bind': binding,
        'color': color,
        'location': location,
        'location_href': location_all_city
    }
    return render(request, 'main/index.html', context)  # return render(request, 'enter/index.html', context)


def main(request):
    category = Category.objects.all()
    services = TypeOfServices.objects.all()
    contact_org = ContactOfOrganization.objects.all()
    color_our = 'radial-gradient(#8cc2cc, transparent)'
    context = {
        'services': services,
        'contact': contact_org,
        'forum': category,
        'color_our': color_our
    }
    return render(request, 'main/about.html', context)


def gallery(request):
    color = 'radial-gradient(#8cc2cc, transparent)'
    if request.user.is_authenticated:
        custom = request.user
        category = Category.objects.all()
        photo_list = PhotoOfWorks.objects.all()
        contact_org = ContactOfOrganization.objects.all()
        favourite = ImageFavorite.objects.filter(owner=custom)
        display = 'block'  # None
        context = {
            'images': photo_list,
            'contact': contact_org,
            'forum': category,
            'display': display,
            'color_gallery': color
        }
        return render(request, 'main/gallery.html', context)
    # custom = request.user
    category = Category.objects.all()
    photo_list = PhotoOfWorks.objects.all()
    contact_org = ContactOfOrganization.objects.all()
    # favourite = ImageFavorite.objects.filter(owner=custom)
    display = None
    context = {
        'images': photo_list,
        'contact': contact_org,
        'forum': category,
        'display': display,
        'color_gallery': color
    }
    return render(request, 'main/gallery.html', context)


def add_favourite(request):  # функция добавления избранных фотографий на AJAX
    if request.method == 'GET':
        custom = User.objects.get(id=request.user.id)  # получаем id пользователя
        image_id_page = request.GET.get('image_id')  # получаем id объекта
        display = '.close-block' + image_id_page
        image = PhotoOfWorks.objects.get(id=image_id_page)
        if custom.imagefavorite_set.filter(image=image_id_page).exists():
            return JsonResponse({'success': False})
        image_favorite = ImageFavorite.objects.create(owner=custom, image=image, knot=True)
        image_favorite.save()
        image.is_favourite = True
        image.save()
        return JsonResponse({'success': True, 'display': display})


def favourite_images(request):  # функция не задействована
    custom = request.user
    images = ImageFavorite.objects.filter(owner=custom)
    context = {
        'images': images
    }
    return render(request, 'main/favourite_images.html', context)


def remove_favourite(request):  # функция удаления выбранных фотографий AJAX
    custom = request.user
    # custom = User.objects.get(id=request.user.id)  получаем id пользователя
    image_id_page = request.GET.get('image_id')
    # display = request.GET.get('display')
    display = '.close-block' + image_id_page
    # print(display)
    # image = PhotoOfWorks.objects.get(id=image_id_page)   получаем id объекта фотографий
    image_favorite = ImageFavorite.objects.get(id=image_id_page)
    image_favorite_id = image_favorite.image
    image = image_favorite.image
    image.is_favourite = False
    image.save()
    image_favorite.delete()
    # images_favorite = ImageFavorite.objects.filter(owner=custom)
    # print(images_favorite)
    # images_favorite = serialize("json", images_favorite)
    # images_favorite = json.loads(images_favorite)
    # display = None
    return JsonResponse({'success': True, 'display': display})  # images_favorite, safe=False, status=200


@login_required(login_url='enter')  # перенаправление незарегистрированных пользователей
def calculate(request):  # форма отправка сообщений с фотографиями
    if request.method == 'POST':
        category = Category.objects.all()
        contact_org = ContactOfOrganization.objects.all()
        # form = ContactForm(request.POST)
        form = ContactForm(request.POST, request.FILES)
        name = request.POST['name']
        content = request.POST['content']
        email = request.POST['email']
        files = request.FILES.getlist('file')
        body = {
            'name': name,
            'email': email,
            'content': content,

        }
        message = '\n'.join(body.values())
        msg = EmailMessage(name, message, email, [settings.EMAIL_HOST_USER])  # settings.EMAIL_HOST_USER, [email]
        for f in files:
            msg.attach(f.name, f.read(), f.content_type)  #
        msg.send()
        context = {
            'form': form,
            'contact': contact_org,
            'forum': category
        }
        messages.success(request, 'Сообщение было отправлено')
        return render(request, 'main/calculate.html', context)

        # else:
        # return render(request, 'main/calculate.html', {'form': form, 'success': 'Повторите отправку'})
    else:
        category = Category.objects.all()
        contact_org = ContactOfOrganization.objects.all()
        form = ContactForm()
        context = {
            'form': form,
            'contact': contact_org,
            'forum': category
        }
        return render(request, 'main/calculate.html', context)


def reviews(request):  # функция вывода отзывов, с пагинацией и поиском на JS
    reviews_all, search_query, info = search_reviews(request)
    custom_range, reviews_all = paginate_reviews(request, reviews_all, 3)
    category = Category.objects.all()
    contact_org = ContactOfOrganization.objects.all()
    context = {
        'reviews': reviews_all,
        'contact': contact_org,
        'forum': category,
        'search_query': search_query,
        'custom_range': custom_range,
        'info': info
    }
    return render(request, 'main/reviews.html', context)


def contact(request):  # функция отправки сообщения на почту без фотографий
    color = 'radial-gradient(#8cc2cc, transparent)'
    if request.method == 'GET':
        category = Category.objects.all()
        contact_org = ContactOfOrganization.objects.all()
        form = SendMessageForm()
        context = {
            'form': form,
            'contact': contact_org,
            'forum': category,
            'color_contact': color
        }
        return render(request, 'main/contact.html', context)
    else:
        form = SendMessageForm()
        category = Category.objects.all()
        contact_org = ContactOfOrganization.objects.all()
        name = request.POST['name']
        organization = request.POST['organization']
        email_from = settings.EMAIL_HOST_USER
        email = request.POST['email']
        content = request.POST['content']
        msg = EmailMessage(name, content, email_from, [email])  # name,  email_from, [email]
        msg.send()
        messages.success(request, 'Сообщение было отправлено')
        context = {
            'form': form,
            'contact': contact_org,
            'forum': category,
            'color_contact': color
        }
        return render(request, 'main/contact.html', context)


def enter(request):
    color = 'radial-gradient(#8cc2cc, transparent)'
    if request.method == 'GET':  # при методе GET возвращаем страницу с формой регистрации
        contact_org = ContactOfOrganization.objects.all()
        context = {
            'form': UserCreationForm(),
            'contact': contact_org,
            'color_enter': color
        }
        return render(request, 'main/enter.html', context)  # модель Form импорт из

        # django.contrib
    else:  # при методе POST регистрируем пользователя со своей проверкой на соответствие паролей и проверкой Django
        # на наличие имени пользователя
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                messages.info(request, 'Вы успешно зарегистрировались')
                return redirect('index')
            except IntegrityError:
                contact_org = ContactOfOrganization.objects.all()
                context = {
                    'form': UserCreationForm(),
                    'error': 'Такое имя пользователя существует выберите другое',
                    'contact': contact_org,
                    'color_enter': color
                }
                return render(request, 'main/enter.html', context)

        else:
            context = {
                'form': UserCreationForm(),
                'error': 'Пароли не совпадают',
                'color_enter': color
            }
            return render(request, 'main/enter.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из сессии')
    return redirect('login')


def login_user(request):
    color = 'radial-gradient(#8cc2cc, transparent)'
    contact_org = ContactOfOrganization.objects.all()
    if request.method == 'GET':  # авторизация зарегистрированного пользователя
        return render(request, 'main/loginuser.html', {'form': AuthenticationForm(), 'contact': contact_org,
                                                       'color_login': color})
    else:  # authenticate метод проверки существующего пользователя
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:  # если user возвращает None, тогда возвращаемся на страницу loginuser.html
            context = {
                'form': AuthenticationForm(),
                'contact': contact_org,
                'color_login': color
            }
            messages.info(request, 'Пользователя с таким именем не существует')
            return render(request, 'main/loginuser.html', context)
        else:  # иначе, сохраняются данные пользователя в серверной части запроса пока пользователь находится в сессии

            login(request, user)
            return redirect('index')


@login_required()
def delete_user(request):  # удаление пользователя
    custom = request.user
    if request.method == 'GET':
        return render(request, 'main/delete.html')
    else:
        custom.delete()
        messages.info(request, 'Аккаунт был успешно удалён')
        return redirect('enter')


# @login_required(login_url='enter')
def calculate_table(request):  # функция калькуляции в виде таблицы checkbox
    contact_org = ContactOfOrganization.objects.all()
    category = Category.objects.all()
    if request.method == 'GET':
        custom = request.user
        if request.user.is_authenticated:
            if custom.pricingandsummworks_set.all().count() < 1:
                form = ListOfWorksForm()
                obj = ListOfWorks.objects.all()
                context = {
                    'form': form,
                    'obj': obj,
                    'contact': contact_org,
                    'forum': category
                }
                return render(request, 'main/calculate_table.html', context)
            else:
                category = Category.objects.all()
                form = ListOfWorksForm()
                obj = ListOfWorks.objects.all()
                context = {
                    'form': form,
                    'obj': obj,
                    'contact': contact_org,
                    'forum': category
                }
                messages.info(request, 'Удалите все расчёты в личном кабинете')
                return render(request, 'main/calculate_table.html', context)
        else:
            messages.info(request, 'форма для незарегистрированных пользователей')
            category = Category.objects.all()
            form = ContactForm()
            obj = ListOfWorks.objects.all()
            context = {
                'form': form,
                'obj': obj,
                'contact': contact_org,
                'forum': category
            }
            return render(request, 'main/calculate.html', context)
    else:
        custom = request.user
        if request.user.is_authenticated and custom.pricingandsummworks_set.all().count() >= 1:
            category = Category.objects.all()
            form = ListOfWorksForm()
            obj = ListOfWorks.objects.all()
            context = {
                'form': form,
                'obj': obj,
                'contact': contact_org,
                'forum': category
            }
            messages.info(request, 'Удалите все расчёты в личном кабинете')
            return render(request, 'main/calculate_table.html', context)
        else:
            cost = cost_works(request)  # функция расчёта стоимости работ находится в utils.py
            category = Category.objects.all()
            obj = ListOfWorks.objects.all()
            form = ContactForm()
            messages.info(request, 'Расчёт был посчитан')
            context = {
                'form': form,
                'obj': obj,
                'contact': contact_org,
                'forum': category
            }
            return render(request, 'main/calculate_table.html', context)


def personal_account(request, pk):  # функция представления личного кабинета
    if request.method == 'GET':
        if request.user.is_authenticated:  # если зарегистрирован пользователь
            context = personal_view(request, pk)
            return render(request, 'main/personal_account.html', context)
        else:  # иначе переход на страницу авторизации
            messages.warning(request, 'Необходимо авторизация или регистрация')
            return redirect('login')

    else:
        if request.POST.get('form_send'):  # отпарвка сообщения на телеграм
            custom = request.user
            if custom.pricingandsummworks_set.filter(owner=custom).exists():  # проверка на существование объекта
                if custom.pricingandsummworks_set.all().count() == 1:
                    message_text = custom.pricingandsummworks_set.all()
                    phone_num = request.user.profileuser.phone_number
                    if phone_num:
                        phone = '\n' + 'Контактный номер: ' + str(phone_num)
                        # message_view = custom.pricingandsummworks_set.get(owner=custom)
                        #  get(owner=custom) берёт один элемент последний
                        #  print(message_view)
                        for i in range(len(message_text)):
                            send_message(message_text[i].estimate + phone)
                        # message = message_text[0].estimate + phone
                        # send_message(message)
                        messages.info(request, 'сообщение было отправлено')
                        context = personal_view(request, pk)
                        return render(request, 'main/personal_account.html', context)
                    else:
                        messages.info(request, 'для отправки необходим номер телефона')
                        context = personal_view(request, pk)
                        return render(request, 'main/personal_account.html', context)
                else:
                    messages.warning(request, 'Отправить можно только один расчёт')
                    context = personal_view(request, pk)
                    return render(request, 'main/personal_account.html', context)
            else:
                messages.info(request, 'У Вас отсутствуют расчёты')
                context = personal_view(request, pk)
                return render(request, 'main/personal_account.html', context)

        elif request.POST.get('delete_pricing'):  # удаление расчёта стоимости работ
            if request.user.is_authenticated:
                custom = request.user
                # message_view = custom.pricingandsummworks_set.get(owner=custom)
                pricing = SummOfWorks.objects.filter(owner=custom)
                pricing_all_text = PricingAndSummWorks.objects.filter(owner=custom)
                pricing_all_text.delete()
                pricing.delete()
                messages.success(request, 'Все расчёты были удалены !')
                context = personal_view(request, pk=custom.id)
                return render(request, 'main/personal_account.html', context)
        elif request.POST.get('forum'):  # создание ветки на форуме
            custom = request.user
            if custom.thread_set.all().count() < 1:
                category = ThreadForm(request.POST)
                if category.is_valid():
                    thread = category.save(commit=False)
                    thread.author = custom
                    thread.save()
                    messages.info(request, 'Раздел был создан можете перейти к обсуждению')
                context = personal_view(request, pk=custom.id)
                return render(request, 'main/personal_account.html', context)
            else:
                messages.info(request, 'Пользователь может создать один форум')
                context = personal_view(request, pk=custom.id)
                return render(request, 'main/personal_account.html', context)
        elif request.POST.get('my_object'):  # POST.get('my_object')
            custom = request.user
            city = request.POST.get('city')
            street = request.POST.get('street')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            types = request.POST.get('types')
            form = MyObjectForm(request.POST, request.FILES)
            if form.is_valid():
                types_service = TypeOfServices.objects.get(id=types)
                owner_object = User.objects.get(id=custom.id)
                my_object = MyObject.objects.create(city=city, street=street,
                                                    description=description, image=image, types=types_service,
                                                    owner=owner_object)
                if LocationObjects.objects.filter(city=city).exists():  # если объект с локацией по этому городу есть,
                    # добавляем его к этой локации
                    loc = LocationObjects.objects.get(city=city)
                    loc.bind.add(my_object)
                    messages.info(request, 'Объект был добавлен')
                    context = personal_view(request, pk=custom.id)
                    return render(request, 'main/personal_account.html', context)
                else:
                    city = request.POST.get('city')
                    city_lower = city.lower()
                    ru_text = translit(city_lower, language_code='ru', reversed=True)
                    download(ru_text, limit=1, output_dir='media/objects', adult_filter_off=True, force_replace=False,
                             timeout=60,
                             verbose=True)
                    loc = LocationObjects.objects.create(city=city, image=f'objects/{ru_text}/image_1.jpg')
                    # если новая локация, то создаём объект "локацию" по названию
                    # города и добавляем его к этой локации
                    loc.bind.add(my_object)
                    # <div id="exampleModalobject" style="display: none"></div
                    messages.info(request, 'Объект был добавлен')
                    context = personal_view(request, pk=custom.id)
                    return render(request, 'main/personal_account.html', context)
            else:
                messages.warning(request, 'Выберите ближайший районный центр, для сохранения объекта')
                context = personal_view(request, pk=custom.id)
                return render(request, 'main/personal_account.html', context)
        else:  # условие выполнения редактирования профиля
            form = UserForm(request.POST, instance=request.user)  # записываем все данные из User в форму
            # также поля из БД Profile
            form_profile = ProfileUserForm(request.POST, request.FILES, instance=request.user.profileuser)
            if form.is_valid():
                custom = request.user
                form_profile.save()
                form.save()  # сохраняем изменения в БД User
                messages.success(request, 'Профиль был успешно изменён')
                # остаёмся на той же странице с отредактированным профилем
                context = personal_view(request, pk)
                return render(request, 'main/personal_account.html', context)
            else:
                #  raise ValueError('ошибка ввода номера')
                messages.info(request, 'неправильный формат номера телефона')
                context = personal_view(request, pk)
                return render(request, 'main/personal_account.html', context)

        context = personal_view(request, pk)
        return render(request, 'main/personal_account.html', context)


def write_reviews(request):
    contact_org = ContactOfOrganization.objects.all()
    category = Category.objects.all()
    if request.method == 'GET' and request.user.is_authenticated:
        custom = request.user
        count_reviews = Review.objects.filter(owner=custom).count()
        if count_reviews < 1:
            u_form = ReviewForm()
            context = {
                'form': u_form,
                'count': count_reviews,
                'forum': category
            }
            messages.info(request, 'Оставить отзыв можно только один раз')
            return render(request, 'main/form_reviews.html', context)
        else:
            category = Category.objects.all()
            u_form = ReviewForm()
            context = {
                'form': u_form,
                'count': count_reviews,
                'contact': contact_org,
                'forum': category
            }
            messages.info(request, 'Вы оставили отзыв, эта форма заполнения вам недоступна')
            return render(request, 'main/form_reviews.html', context)
    else:
        if request.user.is_authenticated:
            category = Category.objects.all()
            custom = request.user
            count_reviews = Review.objects.filter(owner=custom).count()
            review_date = ReviewForm(request.POST, request.FILES)
            if review_date.is_valid() and count_reviews < 1:
                res = review_date.save(commit=False)
                # привязываем пользователя написавшего отзыв к самому отзыву, через связь Foreignkey
                res.owner = request.user
                res.save()
                messages.success(request, 'Отзыв был успешно добавлен')
                return redirect('reviews')
            else:
                u_form = ReviewForm()
                messages.error(request, 'Вы пытаетесь заполнить форму дважды')
                context = {
                    'form': u_form,
                    'contact': contact_org,
                    'forum': category
                }
                return render(request, 'main/form_reviews.html', context)


def delete_pricing(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            custom = request.user
            pricing = SummOfWorks.objects.filter(owner=custom)
            pricing.delete()
            context = personal_view(request, pk=custom.id)
            return render(request, 'main/personal_account.html', context)
    else:
        return redirect(request, 'personal_account')


def price_list(request):
    dismantling = ApartmentPrice.objects.filter(Q(title__startswith='Стен') | Q(title__icontains='демонтаж'))
    plaster = ApartmentPrice.objects.filter(title__startswith='Штукатурка')
    painting = ApartmentPrice.objects.filter(title__startswith='Покраска')
    putty = ApartmentPrice.objects.filter(title__startswith='Шпатлевка')
    wallpaper = ApartmentPrice.objects.filter(title__startswith='Оклейка')
    montage_wall = ApartmentPrice.objects.filter(title__startswith='Монтаж')
    contact_org = ContactOfOrganization.objects.all()
    context = {
        'dismantling': dismantling,
        'plaster': plaster,
        'painting': painting,
        'putty': putty,
        'wallpaper': wallpaper,
        'montage_wall': montage_wall,
        'contact': contact_org
    }
    return render(request, 'main/prise_list.html', context)


def check_username(request):  # проверка имён пользователей на существование htmx
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():  # django метод проверки в БД User
        return HttpResponse('<div id="username-error" class="error_name">Имя не доступно</div>')
    else:
        return HttpResponse('<div id="username-error" class="success_name">Имя доступно</div>')


def found_price(request):  # функция не используется поиск по наименованию работ htmx , вывод текстом
    search = request.GET.get('search')
    if search:
        if ApartmentPrice.objects.filter(Q(title__startswith=search)).exists():
            found = ApartmentPrice.objects.filter(Q(title__iregex=f'{search}'))
            val = found.values_list()
            lst = []
            for i in range(len(val)):
                lst.extend([val[i][1], str(val[i][2]), '\n'])
            # prise = ApartmentPrice.objects.get(id=found.id)
            lst_text = ''.join(lst)
            # print(lst_text)
            return HttpResponse(f'<div class="price_success" id="found-price" >{lst_text}</div>')

        else:
            return HttpResponse('<div class="price_error" id="found_price_none" >Не найдено</div>')

    else:
        return HttpResponse('<div id="found_price_none"></div>')


def found_price_page(request):  # поиск по наименованию работ htmx , вывод в виде таблицы
    search = request.GET.get('search').capitalize()
    if search != '':
        if ApartmentPrice.objects.filter(Q(title__startswith=search)).exists():
            found = ApartmentPrice.objects.filter(Q(title__iregex=f'{search}'))
            context = {
                'found': found
            }
            return render(request, 'main/found.html', context)
        else:
            return HttpResponse('<div id="not" hx-get="/clear/" hx-trigger="load delay:2s">поиск не найден</div>')
    else:
        return HttpResponse('<div id="not" hx-get="/clear/" hx-trigger="load delay:2s">начните поиск</div>')


def clear_tag(request):  # функция убирающая тег messages
    return HttpResponse("")


def calculate_apartments(request):  # функция вывода таблицы для расчёта стоимости работ
    if request.method == 'GET':
        custom = request.user
        if request.user.is_authenticated:
            if custom.pricingandsummworks_set.all().count() < 1:
                price = ApartmentPrice.objects.all()
                contact_org = ContactOfOrganization.objects.all()
                context = {
                    'price': price,
                    'contact': contact_org,
                }
                return render(request, 'main/calculate_apartments.html', context)
            else:
                price = ApartmentPrice.objects.all()
                contact_org = ContactOfOrganization.objects.all()
                context = {
                    'price': price,
                    'contact': contact_org,
                }
                messages.info(request, 'Удалите все расчёты в личном кабинете')
                return render(request, 'main/calculate_apartments.html', context)
        messages.info(request, 'Необходимо зарегистрироваться')
        return redirect('enter')
    else:
        custom = request.user
        if request.user.is_authenticated and custom.pricingandsummworks_set.all().count() >= 1:
            form = ApartmentPriceForm()
            price = ApartmentPrice.objects.all()
            contact_org = ContactOfOrganization.objects.all()
            context = {
                'form': form,
                'price': price,
                'contact': contact_org,
            }
            messages.info(request, 'Удалите все расчёты в личном кабинете')
            return render(request, 'main/calculate_apartments.html', context)
        else:
            cost = cost_works_apartments(request)  # функция расчёта стоимости работ находится в utils.py
            if cost == 'ничего не выбрано':
                form = ApartmentPriceForm()
                price = ApartmentPrice.objects.all()
                contact_org = ContactOfOrganization.objects.all()
                context = {
                    'form': form,
                    'price': price,
                    'contact': contact_org,
                }
                messages.info(request, 'Ничего не выбрано')
                return render(request, 'main/calculate_apartments.html', context)
            form = ApartmentPriceForm()
            price = ApartmentPrice.objects.all()
            contact_org = ContactOfOrganization.objects.all()
            context = {
                'form': form,
                'price': price,
                'contact': contact_org,
            }
            messages.info(request, 'Расчёт произведён и находится в личном кабинете')
            return render(request, 'main/calculate_apartments.html', context)


def data_page(request):  # данные запроса не используется
    host = request.META["HTTP_HOST"]  # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]  # получаем данные браузера
    path = request.path  # получаем запрошенный путь
    #  us = request.path["REMOTE_USER"] аутентификационные данные клиента (при наличии) <p>Data: {us}</p>

    return HttpResponse(f"""
        <p>Host: {host}</p>
        <p>Path: {path}</p>
        
        <p>User-agent: {user_agent}</p>
        
    """)


def create_my_object(request):  # функция создания объекта ремонта помещения htmx
    custom = request.user
    if request.POST:
        city = request.POST.get('city')  # city = check_city(city)
        street = request.POST.get('street')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        types = request.POST.get('types')
        types_service = TypeOfServices.objects.get(id=types)
        owner_object = User.objects.get(id=custom.id)
        my_object = MyObject.objects.create(city=city, street=street,
                                            description=description, image=image, types=types_service,
                                            owner=owner_object)
        if LocationObjects.objects.filter(city=city).exists():  # если объект с локацией по этому городу есть,
            # добавляем его к этой локации
            loc = LocationObjects.objects.get(city=city)
            loc.bind.add(my_object)
            return HttpResponse('')
        else:
            city = request.POST.get('city')
            image = add_image(request, city)
            loc = LocationObjects.objects.create(city=city, image=image)

            # если новая локация, то создаём объект "локацию" по названию
            # города и добавляем его к этой локации
            loc.bind.add(my_object)
            # <div id="exampleModalobject" style="display: none"></div
        return HttpResponse('')
    return HttpResponse('')


def delete_object(request):  # удаление объекта ремонта помещений htmx
    custom = request.user
    # object_id = request.GET.get('object')
    my_object = MyObject.objects.filter(owner=custom)
    my_object.delete()
    return HttpResponse(
        '<h5>Ваш объект ремонта</h5><button type="button" class="btn btn-success" data-bs-toggle="modal"  data-bs-target="#exampleModalobject"> Создатьобъект</button> <div id="see"></div>')


def location_objects(request, pk):
    my_object = LocationObjects.objects.get(city=pk).bind.all()
    contact_org = ContactOfOrganization.objects.all()
    context = {
        'my_object': my_object,
        'contact': contact_org
    }
    return render(request, 'main/location-objects.html', context)


def send_htmx_message(request):  # отправка сообщения вызов обратного звонка при помощи htmx library
    if request.method == 'POST':
        if request.user.is_authenticated:
            message = request.POST['phone']
            message_text = 'Вас просят перезвонить по номеру ' + '\n' + '+7-' + message
            send_message(message_text)
        else:
            return HttpResponse('<div class="footer_wrap" hx-get="/clear/" hx-trigger="load delay:6s">Необходимо '
                                'зарегистрироваться</div>')
    return HttpResponse('<div class="footer_wrap" hx-get="/clear/" hx-trigger="load delay:6s">Сообщение '
                        'отправлено</div>')


def search_city(request):  # проверка на существование города России htmx
    search = request.GET.get('city')
    if search:
        city = check_city(search)  # парсер по списку городов России
        return HttpResponse(f'<div id="check_city" hx-get="/clear/" hx-trigger="load delay:5s">{city}</div>')


def delete_threed(request):  # удаление ветки форума htmx
    custom = request.user
    forum = Thread.objects.get(author=custom)
    forum.delete()
    return HttpResponse('<h6 id="delete-forum" style="display: none"></h6>')


def spinner(request):
    return JsonResponse({'success': True})


def some_view(request):  # функция вывода расчёта стоимости работ в PDF
    contact = ContactOfOrganization.objects.get(id=1)
    company = Company.objects.get(id=1)
    dt = datetime.datetime.today()
    pdfmetrics.registerFont(TTFont('Roboto-Medium', 'main_1/static/font/Roboto-Medium.ttf', 'UTF-8'))
    custom = request.user
    if PricingAndSummWorks.objects.filter(owner=custom).exists():
        order = PricingAndSummWorks.objects.get(owner=custom)  # print(order.estimate)
        ord_str = order.estimate
        # res = []
        # for sub in ord_str:
        # res.append(sub.replace("\n", " "))
        # rus_res = ''.join(res)
        # print(len(rus_res))
        report_derictory = os.path.dirname(reportlab.__file__)  # расположение файла библиотеки reportlab
        fonts = os.path.join(report_derictory, 'fonts')
        custom_font = os.path.join(fonts, 'Roboto-Black_rus.ttf')  # расположение шрифта кириллицы
        rus_font = TTFont("custom-rus", custom_font)
        pdfmetrics.registerFont(rus_font)  # регистрация шрифта
        # lst = list(ord_str)
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, bottomup=1)
        #  p.saveState()
        # p.rotate(180)
        p.drawImage('main_1/static/images/home.ico', 10, 760, width=50, height=50)  # address_icon.png
        #  p.restoreState()
        text = p.beginText(85, 800)
        text.setFont('custom-rus', 16)
        text.textLine(company.title)
        text.setFont('custom-rus', 14)
        text.textLine('Расчёт стоимости работ')
        text.setFont('custom-rus', 11)
        text.textLines(ord_str)
        text.textLine(dt.strftime('%d.%m.%Y %H:%M'))
        text.setFont('custom-rus', 10)
        text.setFillColorRGB(0.5, 0.1, 0)
        text.textLine(contact.address)
        text.textLine(contact.phone)
        text.textLine(contact.email)
        p.drawText(text)
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="Расчёт.pdf")
