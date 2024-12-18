

def myFunc(e):
    return e['year']

cars = [
    {'car': 'bmw', 'year': 2001},
    {'car': "ford", 'year': 2004},
    {'car': "honda", 'year': 2010},
    {'car': "volvo", 'year': 2019} ,
    {'car': "mitsubishi", 'year': 2011},
    {'car': 'audi', 'year': 2007}
]

cars.sort(key=myFunc)
print(cars)
