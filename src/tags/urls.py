from django.urls import path

from .views import create_tag_view, tag_detail_view, tag_image_view

urlpatterns = [
    path("", create_tag_view, name="create_tag"),
    path("<int:tag_id>/", tag_detail_view, name="tag_detail"),
    path("<int:tag_id>/image", tag_image_view, name="tag_image"),
]
