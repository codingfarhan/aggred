from django.shortcuts import render
import datetime
from .models import profile
import uuid 
from django.contrib.auth import authenticate 
from django.conf import settings
from django.core.mail import send_mail




def send_email_after_registration(email, auth_token):

    #### sending email on the given id for verification ####
    
    subject = 'Your Account needs to be verified.'
    message = f'Hey, follow this link to verify your account  http://localhost:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    print(email_from)
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)





def signin(request):

    if request.method == 'POST':

        email = request.POST.get('email', False)
        password = request.POST.get('password', False)

        normal_login = email and password


        if normal_login:

            user = authenticate(email=email, password=password)

            if user is not None:

                return render(request, 'index.html')

            else:

                return render(request, 'error_message.html', {'heading': 'Authentication Failed!', 'message': 'Please re-check your details and try again.'})


        else:

            return render(request, 'error_message.html', {'heading': 'An Error Occured.', 'message': 'Please try again in a moment.'})


    elif request.method == 'GET':

        return render(request, 'signin.html')





def signup(request):



    if request.method == 'POST':

        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        c_password = request.POST.get('c_password', False)

        # google_signup = request['POST'].get(google_signup, False)


        signup_user = email and password and c_password


        if password != c_password:

            return render(request, 'error_message.html', {'heading': 'Error', 'message': 'The passwords you have entered do not match. Please go back and re-enter the details.'})

        elif signup_user:

            # we will signup using our custom user model

            auth_token = str(uuid.uuid4())

            new_user = profile().__class__.objects.create_user(email=email, password=password, full_name='', auth_token = auth_token)

            new_user.save()


            # sending verification mail to the user:

            send_email_after_registration(email, auth_token)


        elif not signup_user:

            return render(request, 'error_message.html', {'heading': 'Error', 'message': 'Please go back and re-check your details.'})

        

    elif request.method == 'GET':

        return render(request, 'signup.html')




def verify_email(request, auth_token):

    if auth_token == request.user.auth_token:

        current_user = profile.__class__.objects.filter(auth_toke=auth_token).first()

        current_user.is_verified = True
        current_user.save()

        return render(request, 'message_screen.html', {'heading': 'Email Successfully Verified!', 'message': 'You will be redirected to the home page in a second.'})
    
    else:

        return render(request, 'error_message.html', {'heading': 'An Error Occured.', 'message': 'Please re-check the URL and try again'})




def settings_(request):

    if request.method == 'GET':

        return render(request, 'settings.html')


def delete_confirmation(request):

    if request.method == 'POST':

        pass

    elif request.method == 'GET':

        return render(request, 'delete_confirmation.html')



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
