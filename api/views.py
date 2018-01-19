from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

def APIResponse(data, message, success):
	settings = {
		"success": success,
		"message": message
	}
	if data is not None:
		return JsonResponse({"data": data, "settings":settings})
	else:
		return JsonResponse({"data": [], "settings": settings})


class WebserverView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(WebserverView, self).dispatch(*args, **kwargs)

	def post(self, request): 
		sql = request.POST.get("sql")
		
		if sql is None or sql == "":
			return APIResponse("", "El parametro 'sql' no tiene datos", 0)
		
		with connection.cursor() as cursor:
			cursor.execute(sql)
			data = cursor.fetchall()
			cursor.close()

		return APIResponse(data, "", 1)

        """
		clave = request.GET.get('clave')
		
		if clave is None:
			return APIResponse("", "Clave vacia", 0)

		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM usuarios WHERE clave = %s", [clave])
			data = cursor.fetchone()
			cursor.close()
			if data is None:
				return APIResponse("", "Usuario incorrecto", 0)

			usuario = [{
				"auto": data[0],
				"nombre": data[1],
				"id": data[3],
				"status": data[5],
				"type": "usuario"
			}]
		return APIResponse(usuario, "Usuario obtenido", 1)
        """
