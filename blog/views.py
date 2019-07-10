from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.parsers import JSONParser
from blog.PostSerializer import PostSerializer
from .models import Post


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
@csrf_exempt
# @renderer_classes((JSONRenderer,))
def post_list(request):
    if request.method == 'GET':
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def post_details(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DosenotExists:
        return HttpResponse(400)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)

# endregion
