from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import response
from rest_framework import status
from products.models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from rest_framework.views import APIView

class ReviewListView(APIView):
    def get(self, request, *args, **kwargs):
        status = request.query_params.get('status', 0)
        page = request.query_params.get('page', 0)
        size = request.query_params.get('size', 20)
        sort = request.query_params.get('sort', 'create_at')
        type = request.query_params.get('type', 'asc')

        reviews = Review.objects.filter(status=status).order_by(f"{sort}" if type == 'asc' else f"-{sort}")[(int(page) - 1) * int(size):int(page) * int(size)]
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReviewDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        page = request.query_params.get('page', 0)
        size = request.query_params.get('size', 20)
        sort = request.query_params.get('sort', 'created_at')
        type = request.query_params.get('type', 'asc')

        review = Review.objects.filter(id=id).order_by(f"{sort}" if type == 'asc' else f"-{sort}")[(int(page) - 1) * int(size):int(page) * int(size)].first()
        if not review:
            return Response({"detail": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReviewByProductView(APIView):
    def get(self, request, product_id, *args, **kwargs):

        page = request.query_params.get('page', 0)
        size = request.query_params.get('size', 20)
        sort = request.query_params.get('sort', 'created_at')
        type = request.query_params.get('type', 'asc')

        is_admin = request.user.is_authenticated and request.user.is_staff

        if is_admin:
            reviews = Review.objects.filter(product_id=product_id).order_by(f"{sort}" if type == 'asc' else f"-{sort}")[(int(page) - 1) * int(size):int(page) * int(size)]
        else:
            reviews = Review.objects.filter(product_id=product_id, status=Review.PUBLISHED).order_by(f"{sort}" if type == 'asc' else f"-{sort}")[(int(page) - 1) * int(size):int(page) * int(size)]

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AuthenticatedUserReviewView(APIView):
    def get(self, request, *args, **kwargs):
        # Query parametrelerini al
        page = request.query_params.get('page', 0)
        size = request.query_params.get('size', 20)
        sort = request.query_params.get('sort', 'created_at')
        type = request.query_params.get('type', 'asc')

        # Kullanıcının oturum açmış olup olmadığını kontrol et
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Veritabanından gerekli incelemeleri çek
        reviews = Review.objects.filter(user_id=request.user, status=Review.PUBLISHED).order_by(f"{sort}" if type == 'asc' else f"-{sort}")[(int(page) - 1) * int(size):int(page) * int(size)]

        # Serializer kullanarak incelemeleri dön
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AuthenticatedUserSingleReviewView(APIView):
    def get(self, request, id, *args, **kwargs):
        page = request.query_params.get('page', 0)
        size = request.query_params.get('size', 20)
        sort = request.query_params.get('sort', 'created_at')
        type = request.query_params.get('type', 'asc')

        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            review = Review.objects.get(id=id, user_id=request.user, status=Review.PUBLISHED)
        except Review.DoesNotExist:
            return Response({"detail": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReviewsByUserView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        # Query parametrelerini al
        page = request.query_params.get('page', 0)
        size = request.query_params.get('size', 20)
        sort = request.query_params.get('sort', 'created_at')
        type = request.query_params.get('type', 'asc')

        # Veritabanından gerekli incelemeleri çek
        reviews = Review.objects.filter(user_id=user_id).order_by(f"{sort}" if type == 'asc' else f"-{sort}")[(int(page) - 1) * int(size):int(page) * int(size)]

        # Serializer kullanarak incelemeleri dön
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateReviewView(APIView):
    def post(self, request, *args, **kwargs):
        # Serializer ile gelen veriyi işle
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Kullanıcı oturum açmış mı kontrol et
            if not request.user.is_authenticated:
                return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Veritabanına yeni inceleme ekleyerek kaydet
            review = serializer.save(user_id=request.user.id, status=Review.NOT_PUBLISHED)
            
            # Oluşturulan incelemeyi serialize edip geri döndür
            response_serializer = ReviewSerializer(review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateReviewView(APIView):
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            review = Review.objects.get(id=id, user_id=request.user)
        except Review.DoesNotExist:
            return Response({"detail": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewUpdateSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            updated_review = serializer.save()
            response_serializer = ReviewSerializer(updated_review)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteReviewView(APIView):
    def delete(self, request, id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authenticated required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            review = Review.objects.get(id=id, user_id=request.user)
        except Review.DoesNotExist:
            return Response({"detail": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        
        deleted_review_data = ReviewSerializer(review).data
        review.delete()

        return Response(deleted_review_data, status=status.HTTP_200_OK)