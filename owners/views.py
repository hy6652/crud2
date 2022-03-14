# from django.shortcuts import render
import json
from django.views import View
from django.http import JsonResponse
from owners.models import Owner, Dog

# Create your views here.
class OwnerView(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data['name']
        email = data['email']
        age = data['age']
        Owner.objects.create(name=name, email=email, age=age)
        return JsonResponse({"message":"created"}, status=201)

    def get(self, request):
        owners = Owner.objects.all()
        result = []
        for owner in owners:
            dogs = [{"name":dog.name, "age":dog.age} for dog in Dog.objects.filter(owner=owner.id)]
            result.append(
                {
                    "name":owner.name,
                    "email":owner.email,
                    "age":owner.age,
                    "dog":dogs
                }
            )
        return JsonResponse({"result":result}, status=200)


class DogView(View):
    def post(self, request):
        data = json.loads(request.body)
        owner = Owner.objects.get(name=data['owner'])
        Dog.objects.create(
            name=data['name'],
            age=data['age'], 
            owner=owner
            )
        return JsonResponse({"result":"created"}, status=201)

    def get(self, request):
        dogs = Dog.objects.all()
        result = []
        for dog in dogs:
            result.append(
                {
                    "name":dog.name,
                    "age":dog.age,
                    "owner":dog.owner.name
                }
            )
        return JsonResponse({"result":result}, status=200)