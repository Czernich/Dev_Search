from django.http import JsonResponse

def getRoutes(request):

    routes = [
        {'GET': '/api/projects'}, #get list of project
        {'GET': '/api/projects/id'}, #get specific project

        {'POST': '/api/projects/id/vote'}, #vote on projects
        {'POST': '/api/users/token'}, #generate token for user/login users
        {'POST': '/api/users/token/refresh'}, #users token expires after 5mins/users can stay logged in
    
    
    ]

    return JsonResponse(routes, safe=False)