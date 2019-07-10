from django.urls import path
from blog import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, \
    post_list,post_details

# class PostSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'date_posted']
#
#
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# router = routers.DefaultRouter()
# router.register('post', PostViewSet)

urlpatterns = [
    # path('', views.home, name='blog-home'), Instead of using function based view now we are using class based view.
    path('', PostListView.as_view(), name='blog-home'),
    path('api/post/', post_list),
    path('api/post/<int:pk>', post_details),
    path('user/<str:username>', UserPostListView.as_view(), name='user-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    # path('api-post/', include(router.urls), name='blog'),
]
