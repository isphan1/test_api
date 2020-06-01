from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .serializers import statusSerializer
from rest_framework.views import APIView
from rest_framework import generics,mixins,permissions,pagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from accounts.api.permissions import IsOwnerOrReadOnly
from .models import Status
from  slugify import slugify
import json
# Create your views here.

def is_json(data):
    try:
        json_data = json.loads(data)
        is_valid = True
    except:
        is_valid = False
    
    return is_valid


class statusListAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = statusSerializer
    search_fields = ('user__username','content')
    ordering_fields = ('user__username','timestamp')
    queryset = Status.objects.all()


    # def get_queryset(self):
    #     request = self.request
    #     qs = Status.objects.all()
    #     query = request.GET.get('q')
    #     if query is not None:
    #         qs = qs.filter(content__icontains=query)
    #     return qs

    # def get_object(self):
    #     request = self.request
    #     passed_id = request.GET.get('id') or self.passed_id
    #     queryset = self.get_queryset()
    #     obj = None

    #     if passed_id is not None:
    #         obj = get_object_or_404(queryset,id=passed_id)
    #         self.check_object_permissions(request,obj)
    #     return obj

    def perform_create(self,serializer):
        slug = slugify(self.request.data['content'][:40])

        serializer.save(user=self.request.user,slug=slug)

    # def perform_update():
    #     pass 

    def get(self,request,*args,**kwargs):
        request = self.request
        url_passed_id = request.GET.get('id')
        json_data = {}
        body_ = request.body

        if is_json(body_):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id',None)

        passed_id = url_passed_id or new_passed_id or None 
        self.passed_id = passed_id

        if passed_id is not None:
            return self.retrieve(request,*args,**kwargs)
        return super().get(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    # def put(self,request,*args,**kwargs):
    #     request = self.request
    #     url_passed_id = request.GET.get('id')
    #     json_data = {}
    #     body_ = request.body

    #     if is_json(body_):
    #         json_data = json.loads(request.body)
    #     new_passed_id = json_data.get('id',None)

    #     passed_id = url_passed_id or new_passed_id or None 
    #     self.passed_id = passed_id

    #     return self.update(request,*args,**kwargs)

    # def patch(self,request,*args,**kwargs):
    #     request = self.request
    #     url_passed_id = request.GET.get('id')
    #     json_data = {}
    #     body_ = request.body

    #     if is_json(body_):
    #         json_data = json.loads(request.body)
    #     new_passed_id = json_data.get('id',None)

    #     passed_id = url_passed_id or new_passed_id or None 
    #     self.passed_id = passed_id


    #     return self.update(request,*args,**kwargs)
    
    # def delete(self,request,*args,**kwargs):

    #     request = self.request
    #     url_passed_id = request.GET.get('id')
    #     json_data = {}
    #     body_ = request.body

    #     if is_json(body_):
    #         json_data = json.loads(request.body)
    #     new_passed_id = json_data.get('id',None)

    #     passed_id = url_passed_id or new_passed_id or None 
    #     self.passed_id = passed_id
    
    #     return self.destroy(request,*args,**kwargs)


    # def get(self,request,format=None):

    #     qs  = Status.objects.all()
    #     serializer = statusSerializer(qs,many=True)

    #     return Response(serializer.data)

# class statusDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = statusSerializer
    # #lookup_field = 'id' #slug

    # def get_object(self,*args,**kwargs):
    #     kwargs = self.kwargs
    #     kw_id = kwargs.get('pk')
    #     return Status.objects.get(pk=kw_id)


class statusDetailAPIView(
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.RetrieveAPIView):

    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    queryset = Status.objects.all()
    serializer_class = statusSerializer
    permission_classes = [IsOwnerOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'


    def perform_update(self,serializer):
        slug = slugify(self.request.data['content'][:40])
        serializer.save(slug=slug)

    def perform_destroy(self,instance):
        if instance is not None:
            return instance.delete()
            return 'Item removed'
        return None

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def patch(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

# class statusCreateAPIView(generics.ListCreateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = statusSerializer

#     # def perform_create(self,serializer):
#     #     serializer.save(user=self.request.user)

    
# class statusUpdateAPIView(generics.RetrieveUpdateAPIView):

#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = statusSerializer

# class statusDeleteAPIView(generics.RetrieveDestroyAPIView):

#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = statusSerializer


