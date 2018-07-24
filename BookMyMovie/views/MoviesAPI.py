from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from BookMyMovie.models import *
from BookMyMovie.serializers import *
from django.http import HttpResponse, JsonResponse

class LocationsListView(APIView):
    def get(self,request,*args,**kwargs):
        LocationsList_object = Locations.objects.values()
        serialized_object = LocationsListSerializer(LocationsList_object, many=True)
        my_dict={'data':serialized_object.data}

        return render(request, 'Home.html', context=my_dict)
        #return JsonResponse(serialized_object.data, safe=False)

    def post(self, request, *args, **kwargs):

        serialized_object = LocationsListSerializer(data=request.POST)
        if serialized_object.is_valid():
            serialized_object.save()
            return JsonResponse(serialized_object.data, status=201)
        return JsonResponse(serialized_object.data, status=400)


class LocationsDetailedView(APIView):
    def get(self,request,*args,**kwargs):
        try:
            LocationsList_object = Locations.objects.values().filter(LocationName=self.kwargs['pk'])
        except Locations.DoesNotExist:
            return HttpResponse(status=404)

        serialized_object = LocationsListSerializer(LocationsList_object, many=True)

        return JsonResponse(serialized_object.data, safe=False)

    def put(self,request,*args,**kwargs):

        try:
            LocationsList_object = Locations.objects.get(LocationName=self.kwargs['pk'])
        except Locations.DoesNotExist:
            return HttpResponse(status=404)

        data = JSONParser().parse(request)

        serialized_object=LocationsListSerializer(LocationsList_object,data=data)
        if serialized_object.is_valid():
            serialized_object.save()
            return JsonResponse(serialized_object.data)
        return JsonResponse(serialized_object.data,status=400)

    def delete(self,request,*args,**kwargs):
        try:
            LocationsList_object = Locations.objects.all().filter(LocationName=self.kwargs['pk'])

            #mocktest_object=mocktest.objects.values('m1','m2','m3','m4','total').filter(student_id=students_object[0]['id'])
        except Locations.DoesNotExist:
            return HttpResponse(status=404)
        LocationsList_object.delete()
        return HttpResponse(status=204)

class MoviesListView(APIView):
    def get(self,request,*args,**kwargs):

        locationlist = Locations.objects.values('id').filter(LocationName=self.kwargs['pk'])
        locationid = locationlist[0]['id']
        MoviesList_object = Movies.objects.all().filter(Location_id=locationid)
        serialized_object = MoviesListSerializer(MoviesList_object, many=True)

        my_dict = {'data': serialized_object.data}

        return render(request, 'Home.html', context=my_dict)
        #return JsonResponse(serialized_object.data, safe=False)

    def post(self, request, *args, **kwargs):

        locationlist=Locations.objects.values('id').filter(LocationName=self.kwargs['pk'])
        locationid=locationlist[0]['id']
        serialized_object = MoviesListSerializer(data=request.data)

        if serialized_object.is_valid():
            serialized_object.save(Location_id=locationid)
            return JsonResponse(serialized_object.data, status=201)
        return JsonResponse(serialized_object.data, status=400)


class MoviesDetailedView(APIView):
    def get(self,request,*args,**kwargs):

        locationlist = Locations.objects.values('id').filter(LocationName=self.kwargs['pk1'])
        locationid = locationlist[0]['id']
        try:
            MoviesList_object = Movies.objects.values().filter(Location_id=locationid ,id=self.kwargs['pk'] )
        except Movies.DoesNotExist:
            return HttpResponse(status=404)

        serialized_object = MoviesListSerializer(MoviesList_object, many=True)

        return JsonResponse(serialized_object.data, safe=False)

    def put(self,request,*args,**kwargs):

        locationlist = Locations.objects.values('id').filter(LocationName=self.kwargs['pk1'])
        locationid = locationlist[0]['id']
        try:
            MoviesList_object = Movies.objects.get(Location_id=locationid ,id=self.kwargs['pk'])
        except Movies.DoesNotExist:
            return HttpResponse(status=404)

        data = JSONParser().parse(request)

        serialized_object=MoviesListSerializer(MoviesList_object,data=data)
        if serialized_object.is_valid():
            serialized_object.save()
            return JsonResponse(serialized_object.data)
        return JsonResponse(serialized_object.data,status=400)

    def delete(self,request,*args,**kwargs):

        locationlist = Locations.objects.values('id').filter(LocationName=self.kwargs['pk1'])
        locationid = locationlist[0]['id']

        try:
            MoviesList_object = Movies.objects.all().filter(Location_id=locationid ,id=self.kwargs['pk'])
        except Movies.DoesNotExist:
            return HttpResponse(status=404)
        MoviesList_object.delete()
        return HttpResponse(status=204)

class TheatresListView(APIView):
    def get(self,request,*args,**kwargs):

        locationlist = Locations.objects.values('id').filter(LocationName=self.kwargs['pk1'])
        locationid = locationlist[0]['id']
        TheatresList_object = Theatres.objects.all().filter(Location_id=locationid,Movie_id=self.kwargs['pk'])
        serialized_object = TheatresListSerializer(TheatresList_object, many=True)

        return JsonResponse(serialized_object.data, safe=False)

    def post(self, request, *args, **kwargs):

        locationlist=Locations.objects.values('id').filter(LocationName=self.kwargs['pk1'])
        locationid=locationlist[0]['id']

        serialized_object = TheatresListSerializer(data=request.POST)

        if serialized_object.is_valid():
            serialized_object.save(Location_id=locationid,Movie_id=self.kwargs['pk'])
            return JsonResponse(serialized_object.data, status=201)
        return JsonResponse(serialized_object.data, status=400)


class TheatresDetailedView(APIView):
    def get(self,request,*args,**kwargs):

        locationlist = Locations.objects.values('id').filter(LocationName=self.kwargs['pk2'])
        locationid = locationlist[0]['id']
        try:
            TheatresList_object = Theatres.objects.values().filter(Location_id=locationid ,Movie_id=self.kwargs['pk1'],id=self.kwargs['pk'] )
        except Theatres.DoesNotExist:
            return HttpResponse(status=404)

        serialized_object = TheatresListSerializer(TheatresList_object, many=True)

        return JsonResponse(serialized_object.data, safe=False)

    def put(self,request,*args,**kwargs):

        locationlist = Locations.objects.values('id').filter(LocationName=self.kwargs['pk2'])
        locationid = locationlist[0]['id']
        try:
            TheatresList_object = Theatres.objects.get(Location_id=locationid ,Movie_id=self.kwargs['pk1'],id=self.kwargs['pk'])
        except Theatres.DoesNotExist:
            return HttpResponse(status=404)

        data = JSONParser().parse(request)

        serialized_object=TheatresListSerializer(TheatresList_object,data=data)
        if serialized_object.is_valid():
            serialized_object.save()
            return JsonResponse(serialized_object.data)
        return JsonResponse(serialized_object.data,status=400)

    def delete(self,request,*args,**kwargs):

        locationlist = Locations.objects.values('id').filter(LocationName=self.kwargs['pk2'])
        locationid = locationlist[0]['id']

        try:
            TheatresList_object = Theatres.objects.all().filter(Location_id=locationid ,Movie_id=self.kwargs['pk1'],id=self.kwargs['pk'])
        except Theatres.DoesNotExist:
            return HttpResponse(status=404)
        TheatresList_object.delete()
        return HttpResponse(status=204)
