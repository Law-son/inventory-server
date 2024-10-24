from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Item, Archive, Category, Unit
from .serializers import ItemSerializer, ArchiveSerializer, CategorySerializer, UnitSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.conf import settings    
from django.db.models import Q

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_items(request):
    """
    Return all items for a particular user.
    """
    user = request.user 
    items = Item.objects.filter(user=user)
    serializer = ItemSerializer(items, many=True)

    if items.exists():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'status': 'error',
                'message': 'No items found for the user'
            },
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_archives(request):
    """
    Return all archives for a particular user.
    """
    user = request.user
    archives = Archive.objects.filter(user=user)
    serializer = ArchiveSerializer(archives, many=True)

    if archives.exists():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'status': 'error',
                'message': 'No archives found for the user'
            },
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_item(request):
    """
    Create a new item for a particular user.
    """
    user = request.user
    data = request.data.copy()
    data['user'] = user.id
    serializer = ItemSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {
                'status': 'error',
                'message': 'Invalid data',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    """
    Update an item for a particular user.
    """
    user = request.user
    item = Item.objects.filter(user=user, id=item_id).first()
    if item is None:
        return Response(
            {
                'status': 'error',
                'message': 'Item not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = ItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'status': 'error',
                'message': 'Invalid data',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def archive_item(request, item_id):
    """
    Archive an item for a particular user.
    """
    user = request.user
    item = Item.objects.filter(user=user, id=item_id).first()
    if item is None:
        return Response(
            {
                'status': 'error',
                'message': 'Item not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    archived_item = Archive(
        user=item.user,
        name=item.name,
        description=item.description,
        barcode=item.barcode,
        category_id=item.category_id,
        quantity=item.quantity,
        price=item.price,
        reorder_quantity=item.reorder_quantity,
        unit_id=item.unit_id,
        date_added=item.date_added,
        last_updated=item.last_updated
    )
    archived_item.save()
    item.delete()
    return Response(
        {
            'status': 'success',
            'message': 'Item archived'
        },
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_all_archives(request):
    """
    Delete all archives for a particular user.
    """
    user = request.user
    archives = Archive.objects.filter(user=user)
    if archives.exists():
        archives.delete()
        return Response(
            {
                'status': 'success',
                'message': 'All archives deleted'
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {
                'status': 'error',
                'message': 'No archives found for the user'
            },
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def restore_all_items(request):
    """
    Restore all archived items for a particular user.
    """
    user = request.user
    archives = Archive.objects.filter(user=user)
    if archives.exists():
        for archive in archives:
            item = Item(
                user=archive.user,
                name=archive.name,
                description=archive.description,
                barcode=archive.barcode,
                category_id=archive.category_id,
                quantity=archive.quantity,
                price=archive.price,
                reorder_quantity=archive.reorder_quantity,
                unit_id=archive.unit_id,
                date_added=archive.date_added,
                last_updated=archive.last_updated
            )
            item.save()
        archives.delete()
        return Response(
            {
                'status': 'success',
                'message': 'All archived items restored'
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {
                'status': 'error',
                'message': 'No archived items found for the user'
            },
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_archive(request, archive_id):
    """
    Delete a particular archive for a particular user.
    """
    user = request.user
    archive = Archive.objects.filter(user=user, id=archive_id).first()
    if archive is None:
        return Response(
            {
                'status': 'error',
                'message': 'No archive found with the given id'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    archive.delete()
    return Response(
        {
            'status': 'success',
            'message': 'Archive deleted'
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def restore_archive(request, archive_id):
    """
    Restore a particular archive back to the items table by id.
    """
    user = request.user
    archive = Archive.objects.filter(user=user, id=archive_id).first()

    if archive is None:
        return Response(
            {
                'status': 'error',
                'message': 'No archive found with the given id'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # Create an item from the archive data
    item = Item(
        user=archive.user,
        name=archive.name,
        description=archive.description,
        barcode=archive.barcode,
        category_id=archive.category_id,
        quantity=archive.quantity,
        price=archive.price,
        reorder_quantity=archive.reorder_quantity,
        unit_id=archive.unit_id,
        date_added=archive.date_added,
        last_updated=archive.last_updated
    )
    item.save()

    # Delete the archive record after restoring
    archive.delete()

    return Response(
        {
            'status': 'success',
            'message': 'Archive restored'
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_categories(request):
    """
    Return all categories for a particular user, including categories with no user.
    """
    user = request.user
    categories = Category.objects.filter(Q(user=user) | Q(user__isnull=True))
    serializer = CategorySerializer(categories, many=True)

    if categories.exists():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'status': 'error',
                'message': 'No categories found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_units(request):
    """
    Return all units for a particular user, including units with no user.
    """
    user = request.user
    units = Unit.objects.filter(Q(user=user) | Q(user__isnull=True))
    serializer = UnitSerializer(units, many=True)

    if units.exists():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'status': 'error',
                'message': 'No units found'
            },
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_category(request):
    """
    Add a particular category for a particular user.
    """
    user = request.user
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        category = Category.objects.filter(Q(user=user), Q(name=serializer.validated_data['name'])).first()
        if category is not None:
            return Response(
                {
                    'status': 'error',
                    'message': 'Category already exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {
                'status': 'error',
                'message': 'Invalid data',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_unit(request):
    """
    Add a particular unit for a particular user.
    """
    user = request.user
    serializer = UnitSerializer(data=request.data)
    if serializer.is_valid():
        unit = Unit.objects.filter(Q(user=user), Q(name=serializer.validated_data['name'])).first()
        if unit is not None:
            return Response(
                {
                    'status': 'error',
                    'message': 'Unit already exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {
                'status': 'error',
                'message': 'Invalid data',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
