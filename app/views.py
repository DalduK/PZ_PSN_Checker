import json
import urllib.request
from datetime import datetime, timezone

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .forms import ItemForm, RegistrationForm, ItemFromURL
from .models import Item, ItemPrice


# Create your views here.


def add_item(request):
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
                item.image = request.POST.get('image')
                item.save()
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
    return render(request, 'items/item.html', {'form': form})


"""
https://store.playstation.com/pl-pl/product/EP0896-CUSA19567_00-RGSUMMERSHIBAINU
https://store.playstation.com/store/api/chihiro/00_09_000/container/PL/pl/999/EP4133-CUSA17438_00-SNOWRUNNERGAME00
"""


def add_item_from_url(request):
    if request.method == 'POST':
        form = ItemFromURL(request.POST)
        if form.is_valid():
            url = request.POST.get('item_url')
            url = url.split('/')[-1]
            respone = urllib.request.urlopen(
                "https://store.playstation.com/store/api/chihiro/00_09_000/container/PL/pl/999/" + url)
            page_source = respone.read()
            data = json.loads(page_source)
            title = data["name"]
            platform = data["playable_platform"][0]
            q = Item.objects.filter(title__iexact=title, platform__exact=platform)
            if len(q) == 0:
                item = Item()
                item.title = title
                if len(data["default_sku"]["rewards"]) == 0:
                    item.price = data["default_sku"]["price"] / 100
                else:
                    item.price = data["default_sku"]["rewards"][0]["price"] / 100
                item.platform = platform
                item.image = data["images"][0]["url"]
                item.age_rating = data["age_limit"]
                item.ps_id = url
                item.save()
                q = Item.objects.filter(title__iexact=title, platform__exact=platform)
            q = q[0]
            qp = ItemPrice.objects.filter(item_id__exact=q.item_id).order_by('-date_fetched')
            if len(qp) > 0:
                print(qp[0].date_fetched)
            if len(qp) == 0 or qp[0].date_fetched < datetime.now(timezone.utc):
                history = ItemPrice()
                history.item_id = q
                print(data["default_sku"])
                if len(data["default_sku"]["rewards"]) == 0:
                    history.historical_price = data["default_sku"]["price"] / 100
                else:
                    history.historical_price = data["default_sku"]["rewards"][0]["price"] / 100
                history.save()
                q.price = history.historical_price
                q.save()
            return HttpResponseRedirect(reverse('base'))
    else:
        form = ItemFromURL()
    return render(request, 'items/itemURLform.html', {'form': form})


def base(request):
    return render(request, 'base.html')


def item_list(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, "home-page.html", context)


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
