from django.shortcuts import render
import datetime




def signin(request):

    if request.method == 'POST':

        pass

    elif request.method == 'GET':

        return render(request, 'signin.html')



def signup(request):

    if request.method == 'POST':

        email = request['POST'].get(email, False)
        password = request['POST'].get(password, False)
        c_password = request['POST'].get(c_password, False)

        google_signup = request['POST'].get(google_signup, False)



        signup_user = email or password or c_password


        if password != c_password:

            return render(request, 'error_message.html', {'heading': 'Error', 'message': 'The passwords you have entered do not match. Please go back and re-enter the details.'})

        elif signup_user:

            # create account using pyrebase API
            
            auth.create_user_with_email_and_password(email, password)

            # store the user's full name in the Firestore Database

            start_date = datetime.datetime.now()

            data = {
                "crowns": "0",
                "email": f"{email}",
                "password": f"{password}",
                "full_name": f"{full_name}",
                "start_date": f"{firebase.database.ServerValue.TIMESTAMP}",
                "title": ""
            }

            database.child("profiles").child("accounts").push(data)


            # signing in the user and verifiying his email:

            user = auth.sign_in_with_email_and_password(email, password)

            auth.send_email_verification(user['idToken'])


        elif not signup_user and not google_signup:

            return render(request, 'error_message.html', {'heading': 'Error', 'message': 'Please go back and re-check your details.'})

        
        elif google_signup:

            pass



        

    elif request.method == 'GET':

        return render(request, 'signup.html')



def settings(request):

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
