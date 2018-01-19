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

    url = "https://api.coinmarketcap.com/v1/ticker/?convert=AUD&limit=20"
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


        numAvailable
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


def view_All(request):
    pass




