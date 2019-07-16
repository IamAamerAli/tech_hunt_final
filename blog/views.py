from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

from blog.PostSerializer import PostSerializer, LoginSerializer, UserSerializer
from blog.permissions import IsOwnerOrReadOnly
from .models import Post
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


# region Views related to website front end

def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/home.html', context)


# region Comments some information
'''
Now we are using class based view. Till now we have used the functions based views like above and below that is 
home and about view. 
We get more functionality whilewe are using the class based view as compare to function based view.
For this example we are using the "list View".  

If we are using the class based view then we also have to make changes in the urls.py file also.
'''


# endregion

class PostListView(ListView):
    model = Post  # The model which we are using to show in list view i.e Post model.
    template_name = 'blog/home.html'
    # <app>/<model>_<viewtype>.html " If the template is named like this we don't have to make the above variable "
    # ex : blog / Post_details.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post  # The model which we are using to show in list view i.e Post model.
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post  # The model which we are using to show in list view i.e Post model.


class PostCreateView(LoginRequiredMixin, CreateView):
    # By using "LoginRequiredMixin" if user is not login the blog cannot be created

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # By using "LoginRequiredMixin" if user is not login the blog cannot be created

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post  # The model which we are using to show in list view i.e Post model.
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# endregion

# region Views related to rest web api
# @csrf_exempt
# def post_list(request):
#     if request.method == 'GET':
#         post = Post.objects.all()
#         serializer = PostSerializer(post, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def post_details(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DosenotExists:
#         return HttpResponse(400)
#
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return JsonResponse(serializer.data)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(post, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         post.delete()
#         return HttpResponse(status=204)
#
# endregion

# region Now here er are using the Request and response Methodology

# @api_view(['GET', 'POST'])
# def post_list(request, format=None):
#     if request.method == 'GET':
#         post = Post.objects.all()
#         serializer = PostSerializer(post, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def post_details(request, pk, format=None):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DosenotExists:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         post.delete()
#         return Response(status=status.HTTP_404_NOT_FOUND)

# endregion

'''
Now above to sections that is 
" Views related to rest web api " and 
" Now here er are using the Request and response Methodology" 
are commented.
Now we are using " Class Based "View instead of function based views  
'''

# region Here for api we are going to use the class based views
# class PostList(APIView):
#
#     def get(self, requset, format=None):
#         post = Post.objects.all()
#         serializer = PostSerializer(post, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PostDetails(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, requst, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=requst.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_404_NOT_FOUND)
# endregion

'''
Now above to sections that is 
" Here for api we are going to use the class based views " is commented.
Now we are using " mixins " instead of class based views  
'''

# region Here for api we are going to use the mixins
# class PostList(mixins.ListModelMixin,
#                mixins.CreateModelMixin,
#                generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#
#     def post(self,request,*args,**kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class PostDetails(mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   generics.GenericAPIView):
#
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
#
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
#
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)
#
# endregion

'''
Now above to sections that is 
" Here for api we are going to use the mixins " is commented.
Now we are using " generic " instead of class based views  
'''


# region Here for api we are going to use the generics
class PostList(generics.ListCreateAPIView):
    lookup_field = 'pk'
    # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # serializer_class = PostAuthSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # serializer_class = PostAuthSerializer


# endregion

# region User authentications Login / Logout
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        # django_login(request, user)
        # for third party ex. android we have to create a token authentication
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


# endregion

# region User Authentication related to post
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class USerDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# endregion
