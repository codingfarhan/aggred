from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profiles.models import profile
import json




@login_required(login_url='signin')
def leaderboards(request, region):

    if request.method == 'GET':


        if region == 'Worldwide':
            result_set = json.dumps(list(profile.objects.all().order_by('crowns')))

        else:
            result_set = json.dumps(list(profile.objects.all().filter(country=region).order_by('crowns')))

        
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


        return render(request, 'leaderboards.html', {'context': context, 'data_available': data_available, 'region': region})