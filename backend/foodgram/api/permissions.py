from rest_framework import permissions


# class IsAuthorOrReadOnly(permissions.BasePermission):

#     message = 'Изменение и удаление запрещено! Вы не являетесь автором рецепта'

#     def has_permission(self, request, view):
#         return super().has_permission(request, view)
    
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.author == request.user
    

class IsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Изменение и удаление запрещено! Вы не являетесь автором рецепта'
    
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)