from django.shortcuts import render
from django.views.generic import TemplateView

import requests
import os
import json
from dotenv import load_dotenv
from covid.settings import BASE_DIR
load_dotenv(os.path.join(BASE_DIR, '.env'))

from datetime import date, timedelta

current_date = date.today().isoformat()
days = [(date.today()-timedelta(days=i)).isoformat() for i in range(61)][::-1]

# Create your views here.


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url1 = "https://covid-193.p.rapidapi.com/statistics"
        url2 = "https://covid-193.p.rapidapi.com/history"

        headers = {
            'x-rapidapi-host': os.environ['x-rapidapi-host'],
            'x-rapidapi-key': os.environ['x-rapidapi-key']
        }

        cases = []
        for day in days:
            querystring = {"day":str(day),"country":"all"}
            response2 = requests.request("GET", url2, headers=headers, params=querystring)
            json_data2 = json.loads(response2.text)
            cases.append(json_data2['response'][-1]['cases']['total'])

        print(cases)
        response1 = requests.request("GET", url1, headers=headers)

        json_data1 = json.loads(response1.text)
        context['days'] = days
        context['cases'] = cases
        context['data2'] = json_data1['response']
        return context
