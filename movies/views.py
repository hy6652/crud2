import json
from django.views import View
from django.http import JsonResponse
from movies.models import Actor, Movie

# Create your views here.
class ActorView(View):
    def post(self, request):
        data = json.loads(request.body)
        Actor.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birt=data['date_of_birt'],
        )

        return JsonResponse({'message':"created"}, status=201)

    def get(self, request):
        actors = Actor.objects.all()
        result = []
        for actor in actors:
            name = actor.first_name + ' ' + actor.last_name
            result.append(
                {
                    "name":name,
                    "date_of_birth":actor.date_of_birt,
                    "movie":[{'movie':movie.title} for movie in actor.movies.all()]
                }
            )
        return JsonResponse({'result':result}, status=200)


class MovieView(View):
    def post(self, request):
        data = json.loads(request.body)
        Movie.objects.create(
            title=data['title'],
            release_date=data['release_date'],
            running_time=data['running_time']
        )
        Actor.objects.get(last_name=data['last_name']).movies.add(Movie.objects.get(title=data['title']))
        return JsonResponse({'message':'created'}, status=201)

    def get(self, request):
        movies = Movie.objects.all()
        result = []

        for movie in movies:
            result.append(
                {
                    'title':movie.title,
                    'running_time':movie.running_time,
                }
            )
        return JsonResponse({'result':result}, status=200)