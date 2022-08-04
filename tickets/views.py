import rest_framework.permissions as p
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import TicketSerializer, TicketUpdateSerializer, UploadTicketPhotoSerializer
from .models import Ticket
import urllib.request
from django.core.files import File
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
@permission_classes([p.AllowAny, ])
def paging_tickets(request, page_num, page_size):
    tickets = Ticket.objects.filter(is_deleted=False).order_by('-id').all()

    serializer = TicketSerializer(list(tickets), many=True)
    paginator = Paginator(serializer.data, page_size)
    try:
        page_tickets = paginator.page(page_num)
    except PageNotAnInteger:
        page_tickets = paginator.page(1)
    except EmptyPage:
        return Response({}, status=status.HTTP_200_OK)

    return Response({"count": paginator.count, "pages_count": paginator.num_pages, "tickets": page_tickets.object_list},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([p.AllowAny, ])
def ticket_list(request):
    tickets = Ticket.objects.filter(is_deleted=False).values()
    return Response(tickets, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([p.AllowAny, ])
def ticket_unresolved_list(request):
    tickets = Ticket.objects.filter(is_deleted=False, state='unresolved').values()
    return Response(tickets, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([p.AllowAny, ])
def ticket_resolved_list(request):
    tickets = Ticket.objects.filter(is_deleted=False, state='resolved').values()
    return Response(tickets, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([p.AllowAny, ])
def ticket_frozen_list(request):
    tickets = Ticket.objects.filter(is_deleted=False, state='frozen').values()
    return Response(tickets, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([p.IsAuthenticated, ])
def my_tickets(request):
    user = request.user
    tickets = Ticket.objects.filter(is_deleted=False, author_id=user).values()
    page_num = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('size', 10))
    paginator = Paginator(tickets, page_size)
    try:
        page_tickets = paginator.page(page_num)
    except PageNotAnInteger:
        page_tickets = paginator.page(1)
    except EmptyPage:
        return Response({}, status=status.HTTP_200_OK)
    return Response(page_tickets.object_list, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([p.IsAuthenticatedOrReadOnly, ])
def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    serializer = TicketSerializer(ticket, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([p.IsAuthenticated, ])
def ticket_new(request):
    serializer = TicketSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([p.IsAuthenticated, ])
def ticket_edit(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if ticket.author.id != request.user.id and not request.user.is_superuser:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = TicketUpdateSerializer(ticket, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([p.IsAuthenticated, ])
def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if ticket.author.id != request.user.id and not request.user.is_superuser:
        return Response(status=status.HTTP_403_FORBIDDEN)
    ticket.is_deleted = True
    ticket.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([p.IsAuthenticated, ])
def upload_ticket_photo(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if not ticket.author.id == request.user.id:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = UploadTicketPhotoSerializer(ticket, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([p.IsAuthenticated, ])
def upload_ticket_photo_from_url(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    photo_url = request.data.get('url')
    result = urllib.request.urlretrieve(photo_url)
    ticket.ticket_photo.save(
        f'{ticket.id}-{os.path.basename(photo_url)}',
        File(open(result[0], 'rb'))
    )
    ticket.save()

    return Response({}, status=status.HTTP_200_OK)
