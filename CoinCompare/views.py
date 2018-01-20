from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views import View
import requests
import json
import math

millnames = ['',' Thousand',' Million',' Billion',' Trillion']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


class HomePage(TemplateView):
    template_name = "index.html"


#next is convert numbers into readable stuff
def index(request):

    url = "https://api.coinmarketcap.com/v1/ticker/?convert=AUD&limit=10"
    respo =  requests.get(url)
    print (respo)
    data = json.loads(respo.content.decode('utf-8'))
    print ("let wjhat data type is? ",type(data[0]))


    count = 0
    print ("value is: ", type(data[1]["max_supply"]))

    for i in data:

        numAvailable = i["available_supply"]
        totalSupply = i["total_supply"]
        maxSupply = i["max_supply"]
        lastHours = i["24h_volume_aud"]
        marketCap = i["market_cap_aud"]
        priceAud = i["price_aud"]

        data[count]["priceAud"] = millify(float(priceAud))
        b = "{:,}".format(float(priceAud))
        c =  b.split(".")
        d = c[0] + "."+c[1][:3]
        data[count]["priceAudReadable"] = d


        data[count]["numAvailable"] = millify(float(numAvailable))
        data[count]["numAvailableReadale"] = "{:,}".format(float(numAvailable))

        data[count]["totalSupply"] = millify(float(totalSupply))
        data[count]["totalSupplyReadale"] = "{:,}".format(float(totalSupply))
        if maxSupply == None:
            data[count]["maxSupply"] = "Null"
            data[count]["maxSupplyReadale"] ="Null"
        else:
            data[count]["maxSupply"] = millify(float(maxSupply))
            data[count]["maxSupplyReadale"] = "{:,}".format(float(maxSupply))

        data[count]["lastHours"] = millify(float(lastHours))
        data[count]["lastHoursReadale"] = "{:,}".format(float(lastHours))

        data[count]["marketCap"] = millify(float(marketCap))
        data[count]["marketCapReadale"] = "{:,}".format(float(marketCap))

        count +=1

    with open('JSONdata.JSON', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    f.close()
    context = {'data': data}
    return render(request, 'index.html', context)


def viewLessMillion(request):

    with open('JSONdata.JSON') as json_data:
        data1 = json.load(json_data)
        data = []
        for i in data1:
            if "Million" in i["numAvailable"]:
                data.append(i)
            else:
                pass

    context = {'data': data}

    return render(request, 'index.html', context)

def viewLesDolar(request):
    with open('JSONdata.JSON') as json_data:
        data1 = json.load(json_data)
        data = []
        for i in data1:
            if float(i["price_aud"]) <= 3:
                data.append(i)
            else:
                pass

    context = {'data': data}

    return render(request, 'index.html', context)

