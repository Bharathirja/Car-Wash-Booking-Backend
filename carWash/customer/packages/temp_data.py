
from datetime import datetime as dt

def booking_temprory(data):
    date = dt.strptime(data['date'], "%b %d %Y")
    return  {
        "vehicle_type":data['vehicle_type'],
        "slot":data['slot'],
        "date":date.date(),
        "area":data['area'],
        "longitude":data['longitude'],
        "latitude":data['latitude'],
        "longitude_delta":data['longitude_delta'],
        "latitude_delta":data['latitude_delta'],
        "booking_amount":data['booking_amount']
    }