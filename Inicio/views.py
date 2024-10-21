from django.shortcuts import render

def loginTemplate(req):
    return render(req,"login.html",{})
