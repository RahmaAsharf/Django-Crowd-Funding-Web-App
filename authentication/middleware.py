# from django.shortcuts import redirect

# class CheckUserIdMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             path_segments = request.path.split('/')
#             if len(path_segments) >= 4 and path_segments[-2].isdigit():
#                 if request.user.id != int(path_segments[-2]):
#                     return redirect('landing')
        
#         response = self.get_response(request)
#         return response
