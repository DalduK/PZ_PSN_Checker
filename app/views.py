from django.shortcuts import render, reverse
from .models import Item, ItemPrice
from django.http import HttpResponseRedirect
from .forms import ItemForm, RegistrationForm
from datetime import datetime, timedelta, timezone
from django.contrib.auth import login, authenticate
from PIL import Image


# Create your views here.


def get_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            title = request.POST.get('item_title')
            platform = request.POST.get('platform')
            q = Item.objects.filter(title__iexact=title, platform__exact=platform)
            if len(q) == 0:
                item = Item()
                item.title = title
                item.price = request.POST.get('item_price')
                item.platform = platform
                q = Item.objects.filter(title__iexact=title, platform__exact=platform)
            q = q[0]
            qp = ItemPrice.objects.filter(item_id__exact=q.item_id).order_by('-date_fetched')
            if len(qp) > 0:
                print(qp[0].date_fetched)
            if len(qp) == 0 or qp[0].date_fetched < datetime.now(timezone.utc):
                history = ItemPrice()
                history.item_id = q
                history.historical_price = request.POST.get('item_price')
                history.save()

                q.price = history.historical_price
                q.save()
            return HttpResponseRedirect(reverse('base'))
    else:
        form = ItemForm()
    return render(request, 'item.html', {'form': form})


def base(request):
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('base'))
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
