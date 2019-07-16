from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from blog import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_view

#     post_list, post_details
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
    # region Web Pages paths
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    # path('api-post/', include(router.urls), name='blog'),
    # endregion

    # region Api Paths

    # region function based view url commented
    #     path('api/post/', post_list),
    #     path('api/post/<int:pk>', post_details),
    # endregion

    # region class based view url commented
    path('api/post/', views.PostList.as_view()),
    path('api/post/<int:pk>', views.PostDetails.as_view()),
    # endregion

    # region Token Authentication paths
    path('api/auth/login/', views.LoginView.as_view()),
    path('api/auth/logout/', views.LogoutView.as_view()),
    # endregion

    # region User Post related paths
    path('api/user/', views.UserList.as_view()),
    path('api/user/<int:pk>', views.USerDetails.as_view()),
    # endregion

    # endregion

]

urlpatterns = format_suffix_patterns(urlpatterns)
