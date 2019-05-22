import logging
import time

from django_filters import FilterSet, DateFilter, DateRangeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login as django_login

from warehouse.kapas.models import User, Customer, Site, DailySiteReading
from warehouse.kapas.serialzers import UserSerializer, TokenSerializer, LoginSerializer, CustomerSerializer, \
    SiteSerializer, DailySiteReadingSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('Total_Property',)
    ordering_fields = ('Total_Property','Name')
    #ordering = ('Name')
    search_fields = ('Name',)


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    #authentication_classes = (TokenAuthentication, SessionAuthentication)
    #permission_classes = (IsAuthenticated,)




class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        print token
        user = User.objects.get(id=token.user_id)
        print user
        serializer = UserSerializer(user, many=False)
        return Response({'token': token.key, 'user': serializer.data})


class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        #django_login(request, user)

        token, created = Token.objects.get_or_create(user=user)

        userInfo = User.objects.get(id=token.user_id)
        serializer = UserSerializer(userInfo, many=False)
        #logger.debug(serializer.data)

        return Response({'token': token.key, 'user': serializer.data})


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    #filter_backend = (DjangoFilterBackend,)
    #filter_class = SiteFilter  # For Filtering in Sites URL

class DailySiteFilter(FilterSet):
    start_date = DateFilter(field_name='Created', lookup_expr='gt',label='Date joined is after (yyyy/mm/dd/):')
    end_date = DateFilter(field_name='Created', lookup_expr='lt',label='Date joined is before (yyyy/mm/dd):')
    date_range = DateRangeFilter(field_name='Created')

    class Meta:
        model = DailySiteReading
        fields = ('Which_Site_reading', 'unit_consumption')


class DailySiteReadingViewSet(viewsets.ModelViewSet):
    queryset = DailySiteReading.objects.all()
    serializer_class = DailySiteReadingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = DailySiteFilter

