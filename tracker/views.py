from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import TransactionForm, ItemForm, UserForm
from .models import Transaction, Item
from django.template.response import TemplateResponse
from django.core.mail import send_mail


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_transaction(request):
    if not request.user.is_authenticated():
        return render(request,'tracker/login.html')
    else:
        form = TransactionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.product_logo = request.FILES['product_logo']
            file_type = transaction.product_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'transaction': transaction,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request,'tracker/create_transaction.html',context)
            transaction.save()
            return render(request, 'tracker/detail.html',{'transaction': transaction})
        context = {
            "form" : form,
        }
        return render(request, 'tracker/create_transaction.html',context)


def create_item(request, transaction_id):
    form = ItemForm(request.POST or None, request.FILES or None)
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if form.is_valid():
        transaction_items = transaction.item_set.all()
        for s in transaction_items:
            if s.product_name == form.cleaned_data.get("product_name"):
                context = {
                    'transaction': transaction,
                    'form': form,
                    'error_message': 'You already added that item',
                }
                return render(request, 'tracker/create_item.html', context)
        item = form.save(commit=False)
        item.transaction = transaction
        item.save()
        return render(request, 'tracker/detail.html', {'transaction': transaction})
    context = {
        'transaction': transaction,
        'form': form,
    }
    return render(request, 'tracker/create_item.html', context)


def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    transaction.delete()
    transaction = Transaction.objects.filter(user=request.user)
    return render(request, 'tracker/index.html', {'transaction': transaction})


def delete_item(request, transaction_id, item_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    item = Item.objects.get(pk=item_id)
    item.delete()
    return render(request, 'tracker/detail.html', {'transaction': transaction})


def detail(request, transaction_id):
    if not request.user.is_authenticated():
        return render(request, 'tracker/login.html')
    else:
        user = request.user
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        return render(request, 'tracker/detail.html', {'transaction': transaction, 'user': user})


def favorite(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    user = request.user
    if user.is_superuser:
        try:
            if item.is_approved:
                item.is_approved = False
            else:
                item.is_approved = True
            item.save()
        except (KeyError, Item.DoesNotExist):
            transaction = Transaction.objects.filter(user=request.user)
            return render(request, 'tracker/index.html', {'transactions': transaction})
        else:
            transaction = Transaction.objects.filter(user=request.user)
            return render(request, 'tracker/index.html', {'transactions': transaction})
    else:
        transaction = Transaction.objects.filter(user=request.user)
        return render(request, 'tracker/index.html', {'transactions': transaction})


def favorite_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    try:
        if transaction.is_approved:
            transaction.is_approved = False
        else:
            transaction.is_approved = True
        transaction.save()
    except (KeyError, Transaction.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'tracker/login.html')
    else:
        transaction = Transaction.objects.filter(user=request.user)
        item_results = Item.objects.all()
        query = request.GET.get("q")
        if query:
            transaction = transaction.filter(
                Q(category_name__icontains=query)
            ).distinct()
            item_results = item_results.filter(
                Q(product_name__icontains=query)
            ).distinct()
            return render(request, 'tracker/index.html', {
                'transactions': transaction,
                'items': item_results,
            })
        else:
            return render(request, 'tracker/index.html', {'transactions': transaction})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'tracker/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                transactions = Transaction.objects.filter(user=request.user)
                return render(request, 'tracker/index.html', {'transactions': transactions})
            else:
                return render(request, 'tracker/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'tracker/login.html', {'error_message': 'Invalid login'})
    return render(request, 'tracker/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                transaction = Transaction.objects.filter(user=request.user)
                return render(request, 'tracker/index.html', {'transaction': transaction})
    context = {
        "form": form,
    }
    return render(request, 'tracker/register.html', context)


def items(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'tracker/login.html')
    else:
        try:
            item_ids = []
            for transaction in Transaction.objects.filter(user=request.user):
                for item in transaction.item_set.all():
                    item_ids.append(item.pk)
            users_items = Item.objects.filter(pk__in=item_ids)
            if filter_by == 'favorites':
                users_items = users_items.filter(is_approved=True)
        except Transaction.DoesNotExist:
            users_items = []
        return render(request, 'tracker/items.html', {
            'item_list': users_items,
            'filter_by': filter_by,
        })


def report_item(request):
    data = Item.objects.all()
    return TemplateResponse(request,'tracker/re.html',{'data':data})


def send_email(request):
    # email_s = EmailMessage()

    subject = request.POST.get('subject', 'Report')
    body = request.POST.get('message', '')
    from_email = settings.EMAIL_HOST_USER
  #  to = request.user.email
    # email_s.attach_file("C:\\atracker - Copy\\tracker\\templates\\tracker\\re.html")
    # email_s.send()

    send_mail(subject=subject, from_email=from_email, recipient_list=['osheen.shrestha@deerwalk.edu.np'], message="http://localhost:8000/tracker/report_item/", fail_silently=False)
    # if subject and message and from_email:
    #     try:
    #         email = EmailMessage(
    #             'Hello',
    #             'Body goes here',
    #             'osheen.shrestha2222052@gmail.com',
    #             [email],
    #         )
    #         email.attach_file("C:\\atracker - Copy\\tracker\\templates\\tracker\\re.html")
    #         email.send()
    #     except BadHeaderError:
    #         return HttpResponse('Invalid header found.')
    #transaction = Transaction.objects.filter(user=request.user)
    return render(request, 'tracker/re.html')
    # else:
        # In reality we'd use a form class
        # to get proper validation errors.
        # return HttpResponse('Make sure all fields are entered and valid.')


    # subject, from_email, to = 'hello', '', email
    # text_content = 'This is an important message.'
    # html_content = '<p>This is an <strong>important</strong> message.</p>'
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()















