from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count, Min, Max
from .models import Prices_db
from django.db import IntegrityError
from binance.client import Client
from django.http import JsonResponse

from mysite.private.api_key import BINANCE_API_KEY, BINANCE_SECRET_KEY

import datetime


def index(request):
    return render(request, 'index.html',)
# Create your views here.


def list_prices(request):
    # prices = Prices_db.objects.all()
    prices = Prices_db.objects.order_by("-open_time")[:25]
    return render(request, 'list_prices.html', {'prices': prices})


def populate(request):

    api_key = BINANCE_API_KEY
    secret_key = BINANCE_SECRET_KEY
    if request.method == 'GET':
        symbol_list = []
        client = Client(api_key, secret_key)
        symbols = client.get_exchange_info()['symbols']
        symbol_list = sorted([symbol['symbol'] for symbol in symbols])
        return render(request, 'populate.html', {'symbol_list': symbol_list})
    if request.method == 'POST':
        print(request.POST)
        symbol = request.POST.get('symbol_list')
        # klines = client.fetch_ohlcv(symbol, '1d')
        # Creare un'istanza di Client di python-binance
        # Inserisci la tua chiave API e la tua chiave segreta


        client = Client(api_key, secret_key)

        interval = request.POST.get('intervals')
        start_time = request.POST.get('start_date')

        klines = client.get_historical_klines_generator(symbol, interval, start_time)

        # Recupera i dati di Kline dall'API Binance
        # klines = client.get_historical_klines_generator(symbol, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
        total = 0
        skipped = 0
        # Itera attraverso i dati di Kline e inseriscili nel database
        for kline in klines:
            total += 1
            open_time = datetime.datetime.fromtimestamp(kline[0] / 1000)
            symbol = symbol
            open_price = kline[1]
            high_price = kline[2]
            low_price = kline[3]
            close_price = kline[4]
            volume = kline[5]
            close_time = datetime.datetime.fromtimestamp(kline[6] / 1000)
            quote_asset_volume = kline[7]
            number_of_trades = kline[8]
            taker_buy_base_asset_volume = kline[9]
            taker_buy_quote_asset_volume = kline[10]
            ignore = kline[11]

            # Controlla se la chiave primaria (open_time e symbol) esiste già
            try:
                prices_db = Prices_db(open_time=open_time, symbol=symbol, open_price=open_price, high_price=high_price,
                                      low_price=low_price, close_price=close_price, volume=volume,
                                      close_time=close_time,
                                      quote_asset_volume=quote_asset_volume, number_of_trades=number_of_trades,
                                      taker_buy_base_asset_volume=taker_buy_base_asset_volume,
                                      taker_buy_quote_asset_volume=taker_buy_quote_asset_volume, ignore=ignore)
                print(f"Record {open_time} {symbol} Inserito in db ")
                prices_db.save()
            except IntegrityError:
                # Se la chiave primaria esiste già, ignorare questa riga di dati
                skipped += 1
                print(f"Record {open_time} {symbol} già presente in db ")
                pass

        prices = Prices_db.objects.order_by("-open_time")[:25]

        print(f"Processo terminato: letti {total} scartati {skipped}")
        return render(request, 'list_prices.html', {'prices': prices, 'total': total,
                                                    'skipped': skipped})


def stats(request):
    symbols = Prices_db.objects.values('symbol').annotate(
        num_records=Count('id'),
        min_date=Min('open_time'),
        max_date=Max('open_time')
    )
    print(symbols)
    return render(request, 'stats.html', {'symbols': symbols})


def delete_all(request):
    Prices_db.objects.all().delete()
    return redirect("list_prices")

def delete_prices(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        Prices_db.objects.filter(symbol=symbol).delete()
        return redirect('stats')
    else:
        symbols = Prices_db.objects.values_list('symbol', flat=True).distinct()
        return render(request, 'delete.html', {'symbols': symbols})


def test_graph(request):
    symbol = 'BTCEUR'
    data = Prices_db.objects.filter(symbol=symbol).values()
    return render(request, 'test_graph.html', {'data': data, 'symbol': symbol})


