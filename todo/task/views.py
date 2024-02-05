from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from task.serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from task.models import TodoTaskModel
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import DestroyAPIView
from task.custom_login_required import IsAuthenticatedAndOwner


class TodoTaskCreateView(APIView):
    
    permission_classes = [IsAuthenticatedAndOwner]
    
    serializer_class = TaskSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            redirect_url = reverse('task_list')
            return redirect(redirect_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        serializer = self.serializer_class()
        return Response({'serializer': serializer.data})
    
    
class ListTaskView(APIView):
    def get(self, request):  
        tasks = TodoTaskModel.objects.all() 
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class UpdateTaskView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticatedAndOwner]
    
    queryset = TodoTaskModel.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "id"
    
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)
    
    
class DeleteTaskView(DestroyAPIView):
    
    permission_classes = [IsAuthenticatedAndOwner]
    
    queryset = TodoTaskModel.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'   
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({"message":"Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
    