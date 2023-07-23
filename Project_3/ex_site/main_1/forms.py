from django import forms
from django.contrib.auth.models import User
from .models import CalculateTableEx, ListOfWorks, ProfileUser, Review, ApartmentPrice, MyObject
from django.forms import ModelForm, ValidationError
import requests
import bs4


class ContactForm(forms.Form):
    name = forms.CharField(max_length=250, label='Ваше имя:')  # disabled=True отключает поле
    email = forms.EmailField(max_length=250, label='Почтовый ящик:')
    content = forms.CharField(widget=forms.Textarea, label='Описание:')  # help_text='текст рядом с полем',
    # strip=True удаление начальных и конечных пробелов
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                  'data-tooltip': 'при отправке нескольких файлов необходимо их выделить'}),
                           label='Выбрать файлы:')

    # square = forms.DecimalField(max_value=1000, min_value=2, label='Укажите площадь помещения:')
    # CHOICES = (
    # ('Paris', 'France'),6LfACDkmAAAAAPlBl1gUHmP4xRrUzDKp7JLw1Y7n
    # ('Moscow', 'Russia'),
    # )
    # position = forms.ChoiceField(choices=CHOICES) choices именованный параметр для тега select в html

    # day = forms.DateField(initial=datetime.date.today) отдельное поле с датой на сегодня


class CalculateTableExForm(ModelForm):  # из django.forms наследуем родительский класс ModelForm для создания Form class
    class Meta:
        model = CalculateTableEx
        fields = ['dismantling', 'montage', 'plaster', 'putty']
        # labels переопределение названия полей
        labels = {'dismantling': 'Демонтаж', 'montage': 'Монтаж', 'plaster': 'Штукатурка', 'putty': 'Шпаклёвка'}


class ListOfWorksForm(ModelForm):
    square = forms.IntegerField(min_value=0, max_value=1000)

    class Meta:
        model = ListOfWorks
        fields = ['title', 'price']


class SendMessageForm(forms.Form):
    '''
    Класс SendMessageForm создаёт форму для отправки от не зарегистрированного клиента сообщения на странице
    contact.html
    '''
    name = forms.CharField(max_length=250, label='Ваше имя:')
    organization = forms.CharField(max_length=250, label='Название организации:')
    email = forms.EmailField(max_length=250, label='Почтовый ящик:')
    content = forms.CharField(widget=forms.Textarea(attrs=({'cols': 50, 'rows': 6})), label='Текст сообщения:')
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    # widget=forms.Textarea,


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']


class UserUpdateForm(forms.ModelForm):  # класс для изменения данных профиля

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ['image', 'phone_number']
        labels = {'image': 'Фотография', 'phone_number': 'Номер телефона'}
        widgets = {
            'phone_number': forms.NumberInput(attrs={
                'pattern': '[9]{1}[0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2}',
                'placeholder': '9234566788, номер начинается с 9'
            })
        }


class ReviewForm(forms.ModelForm):
    # location = forms.CharField(label='Месторасположения объекта работ', required=False)

    class Meta:
        model = Review
        fields = ['description', 'image', 'rating']

        labels = {'description': 'Поле для ввода текста', 'image': 'Выберите фото', 'rating': 'Поставить оценку'}


class ApartmentPriceForm(forms.ModelForm):
    square = forms.IntegerField(min_value=0, max_value=1000)

    class Meta:
        model = ApartmentPrice
        fields = ['title', 'price']


class MyObjectForm(forms.ModelForm):
    def clean_city(self):
        data = self.cleaned_data['city']
        city_check = data.capitalize()
        url = 'https://ru.wikipedia.org/wiki/Список_городов_России'
        request_result = requests.get(url)
        soup = bs4.BeautifulSoup(request_result.text, "html.parser")
        data_lst = []
        table = soup.find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data_lst.append([ele for ele in cols if ele])  # Get rid of empty values

        for i in data_lst:
            if city_check in i:
                return data
        raise ValidationError('Города нет в базе данных')

    class Meta:
        model = MyObject
        fields = ['city', 'street', 'description', 'image', 'types']  # , 'owner'

        labels = {
            'city': 'город',
            'street': 'улица',
            'description': 'Поле для ввода текста',
            'image': 'Выберите фото',
            'types': 'тип ремонта'
        }
