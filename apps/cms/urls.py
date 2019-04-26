from django.urls import path
from . import views

app_name='cms'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('top_category/', views.ProductTopTagManageView.as_view(), name='top_category'),
    path('top_category/<int:top_tag_id>/', views.ProductTopCategoryEditView.as_view(), name='edit_top_category'),
    path('sub_category/',views.ProductSubTagManageView.as_view(),name='sub_category'),
    path('sub_category/<int:sub_tag_id>/',views.ProductSubCategoryEditView.as_view(),name='edit_sub_category'),
    path('add_sub_category/',views.AddSubCategoryView.as_view(),name='add_sub_category'),

    path('add_product/',views.AddProductView.as_view(),name='add_product'),
    path('sub_by_top/<int:top_tag_id>/',views.SubByTopView.as_view(),name='sub_by_top'),
    path('product/manage/', views.ProductManageView.as_view(), name='product_manage'),
    path('product/<int:product_id>/', views.ProductEditView.as_view(), name='product_edit'),

    path('token/', views.QiqiuToken.as_view(), name='upload_token'),  # 上传到七牛
    path('product/images/',views.UploadFdfs.as_view(),name='images'), #上传到FDFS

    path('news/',views.PubNewsView.as_view(),name='pub_news'),
    path('news/manage/',views.NewsManageView.as_view(),name='news_manage'),
    path('news/<int:news_id>/',views.NewsEditView.as_view(),name='news_edit'),

    path('words/',views.WordsView.as_view(),name='words'),

    path('banner/',views.BannerView.as_view(),name='banner'),
]