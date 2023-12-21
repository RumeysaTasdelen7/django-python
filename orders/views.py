import random
import string
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .models import Order, OrderItem, Payment, DiscountLife, Coupons, OrderCoupon
from .serializers import OrderSerializer, OrderDetailSerializer
from orders.permissions import IsAdminOrManager, IsCustomerOrManagerOrAdmin, IsAuthenticated
from rest_framework.permissions import AllowAny

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user_id=user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order_id = self.kwargs.get('id')
        return self.queryset.get(id=order_id)

class CancelOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsCustomerOrManagerOrAdmin]

    def get_object(self):
        order_id = self.kwargs.get('pk')
        try:
            return Order.objects.get(id=order_id, user=self.request.user, status=0)
        except Order.DoesNotExist:
            self.permission_denied(self.request)

    
    def perform_update(self, serializer):
        serializer.save(status='canceled')

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        user_address_id = request.data.get('user_address_id')
        coupon_code = request.data.get('coupon_code')
        payment_data = request.data.get('payment_data')

        order = Order.objects.create(
            session_id=session_id,
            user_address_id=user_address_id,
            coupon_code=coupon_code,
            payment_data=payment_data,
        )

        if coupon_code:
            coupon = get_object_or_404(Coupons, code=coupon_code, status=Coupons.ACTIVE)
            order.discount = coupon.amount
            order.save()

        payment = Payment.objects.create(
            order=order,
            amount=payment_data.get('amount'),
            provider=payment_data.get('provider'),
        )

        serializer = self.get_serializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    


