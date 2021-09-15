from django.shortcuts import render

# Create your views here.



def settings(request):

    if request.method == 'GET':

        return render(request, 'settings.html')


def delete_account(request):

    if request.method == 'POST':

        pass

    elif request.method == 'GET':

        return render(request, 'delete_account.html')



def change_password(request):

    if request.method == 'POST':

        pass

    elif request.method == 'GET':

        return render(request, 'change_password.html')



def change_email(request):

    if request.method == 'POST':

        pass

    elif request.method == 'GET':

        return render(request, 'change_email.html')



def change_title(request):

    if request.method == 'POST':

        pass

    elif request.method == 'GET':

        return render(request, 'change_title.html')



def change_name(request):

    if request.method == 'POST':

        pass

    elif request.method == 'GET':

        return render(request, 'change_name.html')
