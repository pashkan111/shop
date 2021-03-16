from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import CategorySerial
from rest_framework.filters import SearchFilter

from ..models import Category

class CategoryListApi(ListAPIView):

    serializer_class = CategorySerial
    queryset = Category.objects.all()
