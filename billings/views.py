from rest_framework import mixins, permissions, status
from rest_framework import generics
from MyFunctions import permision_chack
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from billings.models import Payment
from billings import serializers
from rest_framework.response import Response


class IsActive(permissions.BasePermission):
    message = ''

    def has_permission(self, request, view):
        message = permision_chack('view', 'user', request.user)['message']
        return permision_chack('view', 'user', request.user)['is_premited']


class BillingsView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSer
    # permission_classes = [WhoCanView]
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = '__all__'

    def get(self, request, *args, **kwargs):
        permission = permision_chack('view', 'payment', request.user)
        if (request.user.id and not permission['is_premited']):
            return Response({"message": permission['message']})
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        permission = permision_chack('add', 'payment', request.user)
        if (request.user.id and not permission['is_premited']):
            return Response({"message": permission['message']})
        return self.create(request, *args, **kwargs)


class BillingView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSer
    # permission_classes = [WhoCanView]

    def get_object(self, pk,):
        try:
            return Payment.objects.get(id=pk)
        except Payment.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        permission = permision_chack('view', 'payment', request.user)
        if (request.user.id and not permission['is_premited']):
            return Response({"message": permission['message']})
        payment = self.get_object(pk)
        serializer = serializers.PaymentSer(payment)
        return Response(serializer.data)

    # def delete(self, request, pk, format=None):
    #     permission = permision_chack('view', 'date', request.user)
    #     if (request.user.id and not permission['is_premited']):
    #         return Response({"message": permission['message']})
    #     date = Date.objects.get(id=pk)
    #     date.objects.filter(id=pk).delete()
    #     serializer = serializers.PaymentSer(date)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        date = self.get_object(pk)
        mySerializer = serializers.PaymentSerForUsers
        if (request.user.is_staff or request.user.is_superuser):
            mySerializer = serializers.PaymentSerForAdmins
        # TODO test
        serializer = mySerializer(
            date, data=request.data)
        permission = permision_chack('change', 'payment', request.user)
        if (not permission['is_premited']):
            return Response({"message": permission['message']})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
