import random
import re
from datetime import datetime, timezone
from pyexpat.errors import messages

import requests
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from plotly.graph_objs import Scatter
from plotly.offline import plot

from MailNotification.MailHandler import MailHandler
from .forms import ItemForm, RegistrationForm, ItemFromURL, Search
from .models import Item, ItemPrice, BasketItem, Carousel


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
        print(form)
        if form.is_valid():
            url = request.POST.get('item_url')
            url = url.split('/')[-1]
            resp= requests.get(
                "https://store.playstation.com/store/api/chihiro/00_09_000/container/PL/pl/999/" + url)
            data = resp.json()
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
                    item.onsale = True
                item.platform = platform
                item.image = data["images"][0]["url"]
                item.age_rating = data["age_limit"]
                item.ps_id = url
                str = data["long_desc"]
                str1 = re.sub('<br.?>',' ', str)
                st = str1.split('.')
                ret = ''
                for i in range(len(st)):
                    if i < 4:
                        print(i)
                        ret = ret + st[i] + '.'
                item.description = ret
                item.tag = data["metadata"]["game_genre"]["values"][0]
                try:
                    item.trailer_url = data["mediaList"]["previews"][0]["url"]
                except KeyError as e:
                    item.trailer_url = data["mediaList"]["screenshots"][0]["url"]
                item.save()
                q = Item.objects.filter(title__iexact=title, platform__exact=platform)
                car = Carousel()
                car.image_url = data["mediaList"]["screenshots"][0]["url"]
                car.save()
            q = q[0]
            qp = ItemPrice.objects.filter(item_id__exact=q.item_id).order_by('-date_fetched')
            car = Carousel()
            car.image_url = data["mediaList"]["screenshots"][3]["url"]
            car.save()
            if len(qp) > 0:
                print(qp[0].date_fetched)
            if len(qp) == 0 or qp[0].date_fetched < datetime.utcnow():
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
            return HttpResponseRedirect(reverse('items'))
    else:
        form = ItemFromURL()
    return render(request, 'items/itemURLform.html', {'form': form})


def base(request):
    return render(request, 'base.html')


def item_list(request):
    sr = Search(request.POST)
    if request.method == 'POST':
        if sr.is_valid():
            ser = request.POST.get('szukaj')
            print(ser)
            items = Carousel.objects.all()
            lista = []
            for i in items:
                lista.append(i.image_url)
            random_items = random.sample(lista, 3)
            numbers_list = Item.objects.filter(title__contains=ser)
            page = request.GET.get('page', 1)
            paginator = Paginator(numbers_list, 12)
            try:
                numbers = paginator.page(page)
            except PageNotAnInteger:
                numbers = paginator.page(1)
            except EmptyPage:
                numbers = paginator.page(paginator.num_pages)
            context = {
                "carousel1": random_items[0],
                "carousel2": random_items[1],
                "carousel3": random_items[2],
                "items": numbers,
                "form": sr
            }
            return render(request, "home-page.html", context)
    else:
        sr = Search(request.POST)
        items = Carousel.objects.all()
        lista = []
        for i in items:
            lista.append(i.image_url)
        random_items = random.sample(lista, 3)
        numbers_list = Item.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(numbers_list, 12)
        try:
            numbers = paginator.page(page)
        except PageNotAnInteger:
            numbers = paginator.page(1)
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)
        context = {
            "carousel1": random_items[0],
            "carousel2": random_items[1],
            "carousel3": random_items[2],
            "items": numbers,
            "form": sr
        }
        return render(request, "home-page.html", context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


def user_watched(request):
    titles = []
    id_list = set()
    current_user = request.user
    user_titles = BasketItem.objects.filter(user_id__exact=current_user.id)
    for title_id in user_titles:
        id_list.add(title_id.item_id.item_id)

    for title_id in id_list:
        q = Item.objects.filter(item_id__exact=title_id)
        for i in q:
            titles.append(i)
    context = {
        "items": titles
    }
    return render(request, "user.html", context)


# def user(request):
#     context = {
#         "items": Item.objects.all()
#     }
#     return render(request, 'user.html')


def register(request):
    mh = MailHandler(587, 'smtp.gmail.com', 'noreply.PSN.Checker@gmail.com', 'Psn12345')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print(username)
            print(user.email)
            mh.sendInvitation(username, user.email)
            login(request, user)
            return HttpResponseRedirect(reverse('items'))
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)


def object_specific_view(request, oid): # The url argument oid is automatically supplied by Django as we defined it carefully in our urls.py\
    if request.user.is_authenticated:
        if request.GET.get("id") != None:
            entry_id = int(request.GET.get("id"))
            print(entry_id)
            basket = BasketItem()
            item = Item.objects.get(item_id=entry_id)
            num_results = BasketItem.objects.filter(item_id=item,user_id=request.user).count()
            if num_results == 0:
                basket.item_id = item
                basket.user_id = request.user
                basket.save()
    if request.user.is_authenticated:
        if request.GET.get("id2") != None:
            entry_id = int(request.GET.get("id2"))
            item = Item.objects.get(item_id=entry_id)
            basket = BasketItem.objects.filter(item_id=item, user_id=request.user)
            basket.delete()
    object = Item.objects.filter(item_id=oid).first()
    if object != None:
        prices = ItemPrice.objects.filter(item_id_id=oid).all()
        price_list = []
        price_data = []
        for i in prices:
            price_list.append(i.historical_price)
            price_data.append(i.date_fetched)
        plt = plot([Scatter(x=price_data, y=price_list,
                            opacity=0.8, marker_color='purple')],
                   output_type='div', config={'displayModeBar': False}, include_plotlyjs=False)
        context= {
            'object': object,
            'plt': plt,
            'x': price_list,
            'y': price_data
        }

        return render(request, "product-page.html", context)
    else:
        items = Carousel.objects.all()
        lista = []
        for i in items:
            lista.append(i.image_url)
        random_items = random.sample(lista, 3)
        numbers_list = Item.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(numbers_list, 12)
        try:
            numbers = paginator.page(page)
        except PageNotAnInteger:
            numbers = paginator.page(1)
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)
        context = {
            "carousel1": random_items[0],
            "carousel2": random_items[1],
            "carousel3": random_items[2],
            "items": numbers
        }
        return render(request, "home-page.html", context)
