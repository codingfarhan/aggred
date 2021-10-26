from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profiles.models import profile
import json
from django.http import Http404, HttpResponseRedirect
import datetime




# helper functions:
def important_details_form(request):

    if request.user.country == '' or request.user.category == '':

        return HttpResponseRedirect('/signup/important_form')

    else:

        pass



def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()






@login_required(login_url='signin')
def leaderboards(request, region):

    if request.method == 'GET':

        important_details_form(request)


        if region == 'Worldwide':
            result_set = json.dumps(list(profile.objects.all().order_by('crowns')), default=myconverter)

        else:
            result_set = json.dumps(list(profile.objects.all().filter(country=region).order_by('crowns')), default=myconverter)

        
        context = []

        qs = json.loads(result_set)

        
        if result_set == '' or len(qs) == 0 or qs[0] == None:
            qs = []

        else:
            rank = 0

            for item in qs:

                rank += 1
                context.append({'full_name': item['full_name'], 'user_image': item['user_image_url'], 'country': item['country'], 'rank': rank, 'crowns': item['crowns']})


        
        if len(context) >= 10:
            context = context[:10]


        if len(context) < 100:
            data_available = False
        else:
            data_available = True

        
        logged_in = request.user.social_user or request.user.is_authenticated

        return render(request, 'leaderboards.html', {'context': context, 'image_url': request.user.user_image_url, 'data_available': data_available, 'region': region, 'logged_in': logged_in})