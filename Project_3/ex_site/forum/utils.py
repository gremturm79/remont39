from .forms import ThreadForm, ReplyForm, CategoryForm
from .models import Thread, Category, Reply
from django.db.models import Q
from main_1.models import ContactOfOrganization
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages


def paginate_forum(request, message, results):
    page = request.GET.get('page', 1)
    # results = 2
    paginator = Paginator(message, results, allow_empty_first_page=True)
    message = paginator.get_page(page)
    left_index = int(page) - 2

    if left_index < 1:
        left_index = 1
    right_index = int(page) + 3
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    custom_range = range(left_index, right_index)
    return custom_range, message


def content(request, pk):
    custom = request.user
    cat = Category.objects.all()
    # cat = custom.thread_set.get()
    # print(cat)
    message = Thread.objects.get(id=pk)
    # response = Reply.objects.get(id=pk)
    response = message.reply_set.all()
    contact_org = ContactOfOrganization.objects.all()
    form = ThreadForm()
    reply = ReplyForm()
    context = {
        'category': cat,
        'reply': reply,
        'form': form,
        'message': message,
        'response': response,
        'contact': contact_org,
    }
    return context


def search_forum(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    message = Thread.objects.filter(Q(title__iregex=search_query) | Q(content__iregex=search_query) |
                                    Q(author__first_name__iregex=search_query) | Q(
        created_at__iregex=search_query) | Q(category__name__iregex=search_query))

    info = True
    if not message.exists():
        message = Thread.objects.all()
        info = messages.info(request, 'по запросу ничего не найдено')

    return message, search_query, info
