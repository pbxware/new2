# coding=utf-8
from suds.client import Client
from delivery.models import City

def run():
    conn = Client("http://couriernew.me-online.ru/Calculator.asmx?wsdl")
    cities = conn.service.Citys()

    for city in cities.diffgram[0][0][0][0]:
        cityName = city.CityRusName[0].encode('utf-8')
        
        newCity= City.objects.create(
            city_code = city.CityCode[0],
            city_name = cityName,
        )
        
        if newCity:
            print "Add city : %s" % cityName

