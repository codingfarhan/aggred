from django.shortcuts import render, redirect
import email
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import post, answer, reply
import uuid
import json
import datetime
from django.http import Http404, HttpResponseRedirect
from profiles.models import profile




def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def get_feedback(name, email, message):

    subject = 'A user wants to contact Aggred.'
    message = message

    email_from = email


    if email_from != False and name != False and message != False:

        send_mail(subject,
        f'This message was sent by {name}, mail id: {email_from}.' + '\n' + '\n' + message,
        email_from,
        [f'{settings.EMAIL_HOST_USER}'],
        fail_silently = False)






def message_screen(request):

    return render(request, 'message_screen.html')





def home(request):

    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        get_feedback(name, email, message)

        heading = 'Thank You For Contacting Us.'
        message = 'Please wait while you are being redirected to the home page.'

        return render(request, 'message_screen.html', {'heading': heading, 'message': message})


    elif request.method == 'GET':


        if request.user.is_active:

            logged_in = True

        else:

            logged_in = False

        return render(request, 'home.html', {'logged_in':logged_in})





@login_required(login_url='signin')
def forum(request):

    if request.method == 'POST':


        # CHECKING IF POST FORM HAS BEEN FILLED:

        title = request.POST.get('title', False)
        explanation = request.POST.get('details', False)
        post_form_submit = request.POST.get('post_question', False)

        post_class = request.POST.get('post_class', False)
        post_subject_or_course = request.POST.get('post_subject_or_course', False)


        print(title, explanation, post_class, post_subject_or_course)

        filled_post_form = title and explanation and post_form_submit



        full_name = request.user.first_name + ' ' + request.user.last_name



        if not filled_post_form:

            return render(request, 'error_message.html', {'heading': 'An Unexpected Error Occured', 'message': 'Please try again later.'})

        elif filled_post_form:

            # if a question is posted:

            if post_form_submit == "posting_question":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, grade=post_class, subject=post_subject_or_course, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation, user_title=request.user.title)
                new_post.save()

                return redirect(f'forum/post/{post_id}')

        else:

            return render(request, 'error_message.html', {'heading': 'Unexpected Error', 'message': 'Please try again in a while'})



    elif request.method == 'GET':

        if request.user.is_verified or request.user.social_user:

            logged_in = True

        else:

            logged_in = False

        return render(request, 'forum.html', {'logged_in': logged_in})






@login_required(login_url='signin')
def category_posts(request, class_, subject, search_query):

    
    if request.method == 'GET':

        search_query = search_query.replace("+", " ")

        print(class_, subject, search_query)

        no_results = 'False'


        # if search_query != " " and education_level == None:

        #     print('search query is ', search_query)

        #     result_set = json.dumps(list(post.objects.filter(post_title=search_query).values()), default=myconverter)

        # elif  search_query == " " and education_level != None:
            
        #     # Here, education_level != "None" means that the user has selected School Level (Since it is the only option) so in this case we will only show results for school level questions

        #     if class_ == None and subject_or_course == None:

        #         print('search query is ', search_query)

        #         result_set = json.dumps(list(post.objects.filter(grade__icontains="Class ").values()), default=myconverter)

        #     elif class_ != None and subject_or_course == None:

        #         print('search query is ', search_query)

        #         result_set = json.dumps(list(post.objects.filter(grade=class_).values()), default=myconverter)

        #     elif class_ != None and subject_or_course != None:

        #         print('search query is ', search_query)

        #         result_set = json.dumps(list(post.objects.filter(grade=class_, subject=subject_or_course).values()), default=myconverter)


        if search_query == "all":

            print('search query is ', search_query)

            result_set = json.dumps(list(post.objects.filter(grade=class_, subject=subject).values()), default=myconverter)

        
        elif search_query != "all":

            print('search query is ', search_query)

            result_set = json.dumps(list(post.objects.filter(grade=class_, subject=subject, post_title__icontains=search_query).values()), default=myconverter)




        context = []

        qs = json.loads(result_set)
        print(qs)


        if result_set == '' or len(qs) == 0 or qs[0] == None:
            qs = []

        else:

            for item in qs:
                context.append({'post_id': item['post_id'], 'email': item['email'], 'user_image_url': item['user_image_url'], 'full_name': item['full_name'], 'user_title': item['user_title'], 'post_title': item['post_title'], 'post_content': item['post_content'], 'likes': item['likes'], 'post_date': item['post_date'], 'answers': item['answers'], 'redirect_url': f"forum/post/{item['post_id']}"})



        if result_set != '' and len(context) == 0:
            no_results = 'True'

        
        logged_in = request.user.is_verified or request.user.social_user
        print(logged_in)

        return render(request, 'category_posts.html', {'context': context, 'search': search_query, 'no_results': no_results, 'number_of_results': len(context), 'logged_in': logged_in})






@login_required(login_url='signin')
def post_id(request, post_id):

    if request.method == 'GET':

        # sending post data:

        post_data = post().__class__.objects.filter(post_id=post_id).first()

        if post_data is None:

            raise Http404("Post does not exist. Are you sure the URL is correct?")

        else:

            already_answered = str(answer.objects.filter(post_id=post_id, email=request.user.email).exists())

        
            full_name = post_data.full_name
            image_url = post_data.user_image_url
            likes = post_data.likes
            title = post_data.post_title
            content = post_data.post_content
            post_date = post_data.post_date
            answers = post_data.answers

            post_id = post_data.post_id

            user_title = post_data.user_title

            post_date = post_data.post_date

            email = post_data.email


            answers_list = []
            replies_list = []


            # sending answer data (if any):

            answers_data = json.dumps(list(answer.objects.filter(post_id=post_id).values()), default=myconverter)

            if answers_data != '':

                qs = json.loads(answers_data)

                print(qs)
                answers_exist = 'True'

                for item in qs:

                    answers_list.append({'full_name': item['full_name'], 'email': item['email'], 'answer_id': item['answer_id'], 'image': item['user_image_url'], 'user_title': item['user_title'], 'answer_title': item['answer_title'], 'answer_content': item['answer_content'], 'time_stamp': item['timestamp'], 'votes': item['votes']})


            else:

                answers_exist = 'False'
            


            # sending replies data (if any):


            replies_data = json.dumps(list(reply.objects.filter(post_id=post_id).values()), default=myconverter)


            if replies_data != '':

                qs = json.loads(replies_data)

                print(qs)
                replies_exist = 'True'

                for item in qs:

                    replies_list.append({'full_name': item['full_name'], 'reply_id': item['reply_id'], 'email': item['email'], 'replying_to': item['replying_to'], 'answer_id': item['answer_id'], 'image': item['user_image_url'], 'reply_content': item['reply_content'], 'time_stamp': item['reply_date']})


            else:

                replies_exist = 'False'


            return render(request, 'post.html', {'current_user': request.user.email, 'email': email, 'already_answered': already_answered, 'answers_exist': answers_exist, 'answers_list': answers_list, 'replies_exist': replies_exist, 'replies_list': replies_list, 'full_name': full_name, 'image_url': image_url, 'likes': likes, 'title': title, 'content': content, 'post_date': post_date, 'answers': answers, 'post_id': post_id, 'user_title': user_title})


    elif request.method == 'POST':


        title = request.POST.get('title', False)
        explanation = request.POST.get('details', False)
        post_form_submit = request.POST.get('submit_btn', False)

        filled_post_form = title and explanation and post_form_submit

        full_name = request.user.first_name + ' ' + request.user.last_name



        # for debugging:

        print('for debugging: ', title, explanation, post_form_submit)


        if not filled_post_form and len(post_form_submit.split(',')) != 3:

            return render(request, 'error_message.html', {'heading': 'An Error Occured', 'message': 'Please try again later.'})

        else:

            # if a question is posted:

            if post_form_submit == "posting_question":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, user_title=request.user.title, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation)
                new_post.save()

                return HttpResponseRedirect(request.path_info)


            elif post_form_submit == "answering_question":

                # saving answer:


                ans_id = str(uuid.uuid4())

                new_ans = answer(post_id=post_id, answer_id=ans_id, full_name=full_name, email=request.user.email, user_title=request.user.title, user_image_url=request.user.user_image_url, answer_title=title, answer_content=explanation)
                new_ans.save()

                return HttpResponseRedirect(request.path_info)

            
            elif post_form_submit.split(',')[0] == "replying_to_answer" or post_form_submit.split(',')[0] == "replying_to_reply":

                # saving reply:

                reply_id = str(uuid.uuid4())

                new_reply = reply(reply_id=reply_id, replying_to=post_form_submit.split(',')[-1], post_id=post_id, answer_id=post_form_submit.split(',')[1], email=request.user.email, user_image_url=request.user.user_image_url, full_name=request.user.first_name + ' ' + request.user.last_name, reply_content=explanation)
                new_reply.save()

                return HttpResponseRedirect(request.path_info)





@login_required(login_url='signin')
def edit_post(request, post_id):

    if request.method == 'GET':

        post_data = post.objects.filter(post_id=post_id).first()

        post_content = post_data.post_content
        post_title = post_data.post_title


        return render(request, 'edit_post.html', {'post_content': post_content, 'post_title': post_title})


    elif request.method == 'POST':

        content = request.POST.get('details', False)
        # title = request.POST.get('title', False)

        post_ = post.objects.filter(post_id=post_id).first()


        # editing values for the post:
        post_.post_content = content
        # post_.post_title = title

        post_.save()

        return HttpResponseRedirect(f'/forum/post/{post_id}')





@login_required(login_url='signin')
def edit_answer(request, answer_id):

    answer_ = answer.objects.filter(answer_id=answer_id).first()

    if request.method == 'GET':


        answer_content = answer_.answer_content
        answer_title = answer_.answer_title

        return render(request, 'edit_answer.html', {'answer_content': answer_content, 'answer_title': answer_title})

    
    elif request.method == 'POST':

        title = request.POST.get('title', False)
        content = request.POST.get('details', False)

        answer_.answer_title = title
        answer_.answer_content = content


        post_id = answer_.post_id
        answer_.save()

        return HttpResponseRedirect(f'/forum/post/{post_id}')




@login_required(login_url='signin')
def edit_reply(request, reply_id):

    reply_ = reply.objects.filter(reply_id=reply_id).first()


    if request.method == 'GET':

        content = reply_.reply_content

        return render(request, 'edit_reply.html', {'reply_content': content})



    elif request.method == 'POST':

        new_content = request.POST.get('details', False)

        reply_.reply_content = new_content
        reply_.save()

        post_id = reply_.post_id

        return HttpResponseRedirect(f'/forum/post/{post_id}')







@login_required(login_url='signin')
def delete_post(request, post_id):


    if request.method == 'GET':

        qs = answer.objects.filter(post_id=post_id)
        delete_ = True

        votes_count = 0

        # can only delete post if there are 0 answers that have been given a lot of votes (we assume that number to be 20 here).

        if qs.exists():

            for item in qs.values():

                votes_count += item['votes']

                if votes_count >= 25:

                    delete_ = False

                    return render(request, 'error_message.html', {'heading': 'Delete Unsuccessful', 'message': 'You cannot delete this question from the forum as a significant number of people have already interacted with it. Do you want to edit it instead?'})


        if delete_ == True:         
        
            return render(request, 'delete_confirmation.html', {'heading': 'Are you sure you want to delete this post?', 'message': 'This is an irreversable action.', 'redirect_path': 'forum'})


    elif request.method == 'POST':


        # delete the post

        del_post = post.objects.filter(post_id=post_id).first()
        del_post.delete()

        # delete all associated answers

        del_answers = answer.objects.filter(post_id=post_id).all()

        for row in del_answers:
            row.delete()

        # delete all associated replies

        del_replies = reply.objects.filter(post_id=post_id).all()

        for row in del_replies:
            row.delete()

        return render(request, 'message_screen.html', {'heading': 'Delete Successful', 'message': 'Your post was successfuly deleted.'})






@login_required(login_url='signin')
def delete_answer(request, answer_id):

    answer_ = answer.objects.filter(answer_id=answer_id).first()

    
    if request.method == 'GET':

        return render(request, 'delete_confirmation.html', {'heading': 'Delete Confirmation', 'message': 'Are you sure you want to delete this answer? This action cannot be reversed.', 'redirect_url': f'forum/post/{answer_.post_id}'})


    elif request.method == 'POST':

        answer_.delete()

        return render(request, 'message_screen.html', {'heading': 'Delete Successful', 'message': 'Your answer was successfully deleted.'})





@login_required(login_url='signin')
def delete_reply(request, reply_id):

    reply_ = reply.objects.filter(reply_id=reply_id).first()


    if request.method == 'GET':

        return render(request, 'delete_confirmation.html', {'heading': 'Delete Confirmation', 'message': 'Are you sure you want to delete this reply?', 'redirect_url': f'forum/post/{reply_.post_id}'})


    elif request.method == 'POST':

        reply_.delete()

        return render(request, 'message_screen.html', {'heading': 'Delete Successful', 'message': 'Your reply was successfully deleted.'})






@login_required(login_url='signin')
def saved_posts(request):

    pass




@login_required(login_url='signin')
def my_posts(request):

    if request.method == 'GET':

        user_email = request.user.email

        posts = json.dumps(list(post.objects.filter(email=user_email).values()), default=myconverter)


        if posts != '':
            qs = json.loads(posts)


        context = []

        
        for item in qs:
            context.append({'post_id': item['post_id'], 'email': item['email'], 'user_image_url': item['user_image_url'], 'full_name': item['full_name'], 'user_title': item['user_title'], 'post_title': item['post_title'], 'post_content': item['post_content'], 'likes': item['likes'], 'post_date': item['post_date'], 'answers': item['answers'], 'redirect_url': f"form/post/{item['post_id']}"})


        no_of_posts = len(context)
        logged_in = request.user.is_verified or request.user.social_user

        return render(request, 'my_posts.html', {'context': context, 'no_of_posts': no_of_posts, 'logged_in': logged_in}) 