from django.shortcuts import render, get_object_or_404, redirect
from main_1.models import ContactOfOrganization
from .models import Category, Thread, Reply
from .forms import ThreadForm, ReplyForm
from django.contrib import messages
from .utils import content, search_forum, paginate_forum


def index(request):
    message, search_query, info = search_forum(request)
    custom_range, message = paginate_forum(request, message, 2)
    contact_org = ContactOfOrganization.objects.all()
    context = {
        'custom_range': custom_range,
        'message': message,
        'search_query': search_query,
        'contact': contact_org,
        'info': info
    }
    return render(request, 'forum/index.html', context)


def forum(request, pk):
    if request.method == 'GET':
        context = content(request, pk)
        message = Thread.objects.get(id=pk)
        return render(request, 'forum/forum.html', context)
    else:
        custom = request.user
        # thread = get_object_or_404(Thread, pk=pk)
        message = Thread.objects.get(id=pk)
        # category = get_object_or_404(Category, pk=pk)
        context = content(request, pk)
        if request.POST.get('write'):  # открытие нового раздела
            if request.user.is_authenticated:
                form = ThreadForm(request.POST)
                if form.is_valid():
                    thread = form.save(commit=False)
                    # thread.category = category  # сохраняем категорию по pk
                    thread.author = custom  # сохраняем автор по user
                    thread.save()
                    return render(request, 'forum/forum.html', context)
                else:
                    return render(request, 'forum/forum.html', context)
            messages.info(request, 'Только для зарегистрированных пользователей')
            return render(request, 'forum/forum.html', context)
        if request.POST.get('reply'):  # сообщения по разделам
            if request.user.is_authenticated:
                custom = request.user
                form = ReplyForm(request.POST)
                if form.is_valid():
                    reply = form.save(commit=False)
                    # print(message)
                    # reply.content = request.POST['content']
                    # print(reply.content)
                    reply.tread = message
                    # print(reply.tread)
                    reply.author = custom
                    reply.save()
                    return render(request, 'forum/forum.html', context)
                else:
                    messages.info(request, 'Отправка сообщений только для зарегистрированных пользователей')
                    return render(request, 'forum/forum.html', context)
            else:
                messages.info(request, 'Отправка сообщений только для зарегистрированных пользователей')
                return render(request, 'forum/forum.html', context)
    return render(request, 'forum/forum.html', context)
