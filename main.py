#!/usr/bin/env python

# Gets Bitcoin rates from Coindesk and re-exports to Prometheus

from requests import get
from prometheus_client import CollectorRegistry, Gauge, start_http_server
from time import sleep
import argparse

URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
BTC = Gauge('BTC', 'Bitcoin to currency rates', ['currency'])

def fetch(URL):
    r = get(URL)
    return r.json()

def main(port = 8080):
    start_http_server(port)
    while 1:
        print('Fetching...')
        data = fetch(URL)
        BTC.labels(currency='USD').set(data['bpi']['USD']['rate_float'])
        BTC.labels(currency='GBP').set(data['bpi']['GBP']['rate_float'])
        BTC.labels(currency='EUR').set(data['bpi']['EUR']['rate_float'])
        sleep(15)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="BTC Prometheus Exporter")
    parser.add_argument('--port', type=int, help='Listening port for scraper (Default: 8080)', required=False)
    args = parser.parse_args()
    if args.port:
        main(args.port)
    else:
        main()