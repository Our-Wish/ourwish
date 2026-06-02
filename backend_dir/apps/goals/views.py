from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Goal
from .serializers import GoalSerializer


# Create your views here.
class GoalCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(member=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoalLatestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        goal = Goal.objects.filter(member=request.user).order_by("-created_at").first()
        if goal is None:
            return Response(None)
        serializer = GoalSerializer(goal)
        return Response(serializer.data)
