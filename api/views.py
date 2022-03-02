from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/projects'}, #get list of project
        {'GET': '/api/projects/id'}, #get specific project

        {'POST': '/api/projects/id/vote'}, #vote on projects
        {'POST': '/api/users/token'}, #generate token for user/login users
        {'POST': '/api/users/token/refresh'}, #users token expires after 5mins/users can stay logged in
    
    
    ]

    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    print('USER: ', request.user)
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    
    return Response(serializer.data)