from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Author
from django.views.decorators.csrf import csrf_exempt
import json


class AuthorREST(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, id=None):

        if id is None:  # Проверяем, что требуется вернуть всех пользователей
            data = []
            for author in Author.objects.all():
                # Производим сериализацию, т.е. определяем, что именно запишется в данные для преобразования в JSON
                data_author = {'id': author.id,
                               'name': author.name,
                               'email': author.email}
                data.append(data_author)
        else:
            author = Author.objects.filter(id=id)
            if author:  # Если автор такой есть, т.е. QuerySet не пустой
                author = author.first()  # Получаем первого автора из QuerySet, так как он там один
                # Производим сериализацию, т.е. определяем, что именно запишется в данные для преобразования в JSON
                data = {'id': author.id,
                        'name': author.name,
                        'email': author.email}
            else:  # Иначе, так как автор не найден (QuerySet пустой), то возвращаем ошибку, с произвольным текстом,
                # для понимания почему произошла ошибка
                return JsonResponse({'error': f'Автора с id={id} не найдено!'},
                                    status=404,
                                    json_dumps_params={"ensure_ascii": False,
                                                       "indent": 4}
                                    )

        # После того как данные для ответа созданы - возвращаем Json объект с данными
        return JsonResponse(data, safe=False, json_dumps_params={"ensure_ascii": False,
                                                                 "indent": 4})

    def post(self, request):
        try:
            data = json.loads(request.body)
            author = Author.objects.create(name=data['name'], email=data['email'])
            author.clean_fields()  # Запуск валидаций
            author.save()  # Сохранение в БД

            response_data = {
                'message': f'Автор успешно создан',
                'id': author.id,
                'name': author.name,
                'email': author.email
            }
            return JsonResponse(response_data, status=201,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4}
                                )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4}
                                )
