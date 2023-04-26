from django.shortcuts import redirect
from rest_framework import permissions


class IsOwnerOrRedirect(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Se a solicitação for um método seguro (GET, HEAD ou OPTIONS), permita que todos visualizem o objeto
        if request.method in permissions.SAFE_METHODS:
            return True

        # Se a solicitação for para um objeto que pertence ao usuário logado, permita que o usuário edite o objeto
        if obj.owner == request.user:
            return True

        # Caso contrário, redirecione o usuário para outra página
        return redirect('http://127.0.0.1:8000/api/transactions/contract/list/')
