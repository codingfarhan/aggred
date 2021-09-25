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

        return render(request, 'home.html', {'logged_in': f'{logged_in}'})



@login_required(login_url='signin')
def forum(request):

    if request.method == 'POST':


        title = request.POST.get('title', False)
        explanation = request.POST.get('details', False)
        form_submit = request.POST.get('submit_btn', False)

        print(title, explanation, form_submit)

        valid_ = title and explanation and form_submit

        full_name = request.user.first_name + ' ' + request.user.last_name



        if not valid_:

            return render(request, 'error_message.html', {'heading': 'An Error Occured', 'message': 'Please try again later.'})

        else:

            # if a question is posted:

            if form_submit == "posting_question":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation, user_title=request.user.title)
                new_post.save()

                return redirect(f'forum/post/{post_id}')



    elif request.method == 'GET':

        if request.user.is_verified:

            logged_in = 'True'

        elif profile().__class__.objects.filter(email=request.user.email).exists():

            logged_in = 'True'

        else:

            logged_in = 'False'

        return render(request, 'forum.html', {'logged_in': logged_in})




@login_required(login_url='signin')
def category_posts(request):

    pass



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




            answers_list = []
            replies_list = []


            # sending answer data (if any):

            answers_data = json.dumps(list(answer.objects.filter(post_id=post_id).values()), default=myconverter)

            if answers_data != '':

                qs = json.loads(answers_data)

                print(qs)
                answers_exist = 'True'

                for item in qs:

                    answers_list.append({'full_name': item['full_name'], 'answer_id': item['answer_id'], 'image': item['user_image_url'], 'user_title': item['user_title'], 'answer_title': item['answer_title'], 'answer_content': item['answer_content'], 'time_stamp': item['timestamp'], 'votes': item['votes']})


            else:

                answers_exist = 'False'
            


            # sending replies data (if any):


            replies_data = json.dumps(list(reply.objects.filter(post_id=post_id).values()), default=myconverter)


            if replies_data != '':

                qs = json.loads(replies_data)

                print(qs)
                replies_exist = 'True'

                for item in qs:

                    replies_list.append({'full_name': item['full_name'], 'replying_to': item['replying_to'], 'answer_id': item['answer_id'], 'image': item['user_image_url'], 'reply_content': item['reply_content'], 'time_stamp': item['reply_date']})


            else:

                replies_exist = 'False'


            return render(request, 'post.html', {'current_user': request.user.first_name + ' ' + request.user.last_name, 'already_answered': already_answered, 'answers_exist': answers_exist, 'answers_list': answers_list, 'replies_exist': replies_exist, 'replies_list': replies_list, 'full_name': full_name, 'image_url': image_url, 'likes': likes, 'title': title, 'content': content, 'post_date': post_date, 'answers': answers, 'post_id': post_id, 'user_title': user_title})


    elif request.method == 'POST':


        title = request.POST.get('title', False)
        explanation = request.POST.get('details', False)
        form_submit = request.POST.get('submit_btn', False)

        valid_ = title and explanation and form_submit

        full_name = request.user.first_name + ' ' + request.user.last_name



        # for debugging:

        print('for debugging: ', title, explanation, form_submit)


        if not valid_ and len(form_submit.split(',')) != 3:

            return render(request, 'error_message.html', {'heading': 'An Error Occured', 'message': 'Please try again later.'})

        else:

            # if a question is posted:

            if form_submit == "posting_question":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, user_title=request.user.title, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation)
                new_post.save()

                return HttpResponseRedirect(request.path_info)


            elif form_submit == "answering_question":

                # saving answer:


                ans_id = str(uuid.uuid4())

                new_ans = answer(post_id=post_id, answer_id=ans_id, full_name=full_name, email=request.user.email, user_title=request.user.title, user_image_url=request.user.user_image_url, answer_title=title, answer_content=explanation)
                new_ans.save()

                return HttpResponseRedirect(request.path_info)

            
            elif form_submit.split(',')[0] == "replying_to_answer" or form_submit.split(',')[0] == "replying_to_reply":

                # saving reply:

                reply_id = str(uuid.uuid4())

                new_reply = reply(reply_id=reply_id, replying_to=form_submit.split(',')[-1], post_id=post_id, answer_id=form_submit.split(',')[1], email=request.user.email, user_image_url=request.user.user_image_url, full_name=request.user.first_name + ' ' + request.user.last_name, reply_content=explanation)
                new_reply.save()

                return HttpResponseRedirect(request.path_info)





@login_required(login_url='signin')
def delete_post(request, post_id):


    if request.method == 'GET':

        qs = answer.objects.filter(post_id=post_id)
        delete_ = True

        # can only delete post if there are 0 answers that have been given a lot of votes (we assume that number to be 20 here).

        if qs.exists():

            for item in qs.values():

                if item['votes'] >= 25:

                    delete_ = False

                    return render(request, 'error_message.html', {'heading': 'Delete Unsuccessful', 'message': 'You cannot delete this question from the forum as a significant number of people have already interacted with it.'})


        if delete_ == True:         
        
            return render(request, 'delete_confirmation.html', {'heading': 'Are you sure you want to delete this post?', 'message': 'This is an irreversable action.'})


    elif request.method == 'POST':


        # delete the post

        del_post = post.objects.filter(post_id=post_id).first()
        del_post.delete()

        # delete all associated answers

        del_answers = post.objects.filter(post_id=post_id).all()

        for row in del_answers:
            row.delete()

        # delete all associated replies

        del_replies = reply.objects.filter(post_id=post_id).all()

        for row in del_replies:
            row.delete()

        return HttpResponseRedirect('forum')



@login_required(login_url='signin')
def edit_post(request):

    pass








@login_required(login_url='signin')
def saved_posts(request):

    pass




@login_required(login_url='signin')
def my_posts(request):

    pass