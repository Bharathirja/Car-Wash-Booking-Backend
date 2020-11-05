
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import CustomerProfile
from ..serializer import CustomerSerializer
from django.http import Http404
from rest_framework import permissions, status, generics,viewsets

class CustomerProfileView(APIView):
    
    permission_classes = [ IsAuthenticated ]

    def get_object(self, email):
        try:
            # print(email)
            return CustomerProfile.objects.get(email=email)
        except CustomerProfile.DoesNotExist:
            raise  Http404

    def get(self, request, email, format=None):
        try:
            customer = self.get_object(email)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as  err:
            return Response({'detail':str(err)})
    
    def post(self, request, format=None):
        try:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                # print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            # print(str(err))
            return Response({'detail':str(err)})

    def put(self, request, email, format=None):
        customer = self.get_object(email)
        # print(request.data)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)