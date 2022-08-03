import rest_framework.permissions as p
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Answer
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


@api_view(['GET'])
@permission_classes([p.AllowAny, ])
def answer_list(request):
    answers = Answer.objects.filter(is_deleted=False).values()
    return Response(answers, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([p.AllowAny, ])
def answer_detail(request, id):
    answer = get_object_or_404(Answer, id=id)
    serializer = AnswerSerializer(answer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([p.IsAuthenticated, ])
def answer_new(request):
    serializer = AnswerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ticket_id = request.data.get("ticket_id")
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.author.id != request.user.id and not request.user.is_superuser:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer.save(author=request.user, ticket=ticket)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([p.IsAuthenticated, ])
def answer_edit(request, id):
    answer = get_object_or_404(Answer, id=id)
    if answer.author.id != request.user.id and not request.user.is_superuser:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = AnswerUpdateSerializer(answer, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([p.AllowAny, ])
def ticket_answers(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    answers = Answer.objects.filter(is_deleted=False, ticket_id=ticket.id).values()
    return Response({"answers": answers}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([p.IsAuthenticated, ])
def answer_delete(request, id):
    answer = get_object_or_404(Answer, id=id)
    if answer.author.id != request.user.id and not request.user.is_superuser:
        return Response(status=status.HTTP_403_FORBIDDEN)
    answer.is_deleted = True
    answer.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
