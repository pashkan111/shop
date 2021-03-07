from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import CategorySerial, NotebookSerial, SmartphoneSerial
from rest_framework.filters import SearchFilter

from ..models import Category, Notebook, Smartphone

class CategoryListApi(ListAPIView):

    serializer_class = CategorySerial
    queryset = Category.objects.all()

class NotebookListApi(ListAPIView):

    serializer_class = NotebookSerial
    queryset = Notebook.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'price']
    

class NotebookDetail(RetrieveAPIView):
    serializer_class = Notebook
    queryset = Notebook.objects.all()
    # lookup_field = 'id'


class SmartphoneListApi(ListAPIView):

    serializer_class = SmartphoneSerial
    queryset = Smartphone.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'price']

class SmartphoneDetail(RetrieveAPIView):
    serializer_class = Smartphone
    queryset = Smartphone.objects.all()
    lookup_field = 'name'