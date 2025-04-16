from django.http import HttpResponse

def home(request):
    return HttpResponse("Добро пожаловать на мой сайт!")
def catalog_view(request):
    return HttpResponse("Добро пожаловать на каталог")