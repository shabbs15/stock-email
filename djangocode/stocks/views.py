import re
from django.http import HttpResponse
from django.template import loader

from .models import User

def index(request):
    template = loader.get_template('stocks/index.html')
    return HttpResponse(template.render(request=request))

def wait(request):
    if request.method == "POST":
        password = request.POST["password"]
        email = request.POST["email"]
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse("shit not valid")
        else:
            if User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists homenoy sorry")
            else:
                User.objects.create(email=email, password=password)
                return HttpResponse("pass")
    else:
        return HttpResponse("the fuck you trna do?")
