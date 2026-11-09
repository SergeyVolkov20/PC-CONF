from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render

from .models import (
    User, Category, Product, Build, BuildItem, Order, Review
)
from .serializers import (
    UserSerializer, RegisterSerializer, CategorySerializer,
    ProductListSerializer, ProductDetailSerializer, ProductCreateSerializer,
    BuildSerializer, BuildItemSerializer, OrderSerializer, ReviewSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .services import CompatibilityChecker, recalculate_build



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user




class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('specifications')
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['category', 'brand']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductCreateSerializer




class BuildViewSet(viewsets.ModelViewSet):
    serializer_class = BuildSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Build.objects.filter(user=self.request.user).prefetch_related('items__product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        build = self.get_object()
        serializer = BuildItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data.get('quantity', 1)
            item, created = BuildItem.objects.update_or_create(
                build=build, product=product,
                defaults={'quantity': quantity}
            )
            recalculate_build(build)
            return Response(BuildItemSerializer(item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, pk=None, item_id=None):
        build = self.get_object()
        BuildItem.objects.filter(build=build, id=item_id).delete()
        recalculate_build(build)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def compatibility(self, request, pk=None):
        build = self.get_object()
        checker = CompatibilityChecker(build)
        return Response(checker.check_all())



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Review.objects.filter(is_approved=True).select_related('user', 'product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




def index_view(request):
    return render(request, 'someapp/index.html')

def login_view(request):
    return render(request, 'someapp/login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/login/')

def register_view(request):
    return render(request, 'someapp/register.html')

def configurator_view(request):
    return render(request, 'someapp/configurator.html')

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def web_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    from django.contrib.auth import authenticate
    user = authenticate(username=email, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id
        })
    return Response({'error': 'Неверный email или пароль'}, status=401)