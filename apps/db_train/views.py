from django.shortcuts import render
from django.views import View
from .models import Author, AuthorProfile, Entry, Tag
from django.db.models import Q, Max, Min, Avg, Count

class TrainView(View):
    def get(self, request):
        # Создайте здесь запросы к БД
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])  # Какие авторы имеют самую высокую уровень самооценки(self_esteem)?
        # count_author_entries = Author.objects.annotate(number_of_entries=Count('entries')).values('username', 'number_of_entries')
        max_entries = Author.objects.aggregate(max_entries=Max('entries'))
        self.answer2 = Author.objects.get(entries=max_entries['max_entries'])  # Какой автор имеет наибольшее количество опубликованных статей?
        cinema_id = Tag.objects.get(name='Кино')
        music_id = Tag.objects.get(name='Музыка')
        self.answer3 = Entry.objects.filter(tags__in=[cinema_id, music_id]).distinct()  # Какие статьи содержат тег 'Кино' или 'Музыка' ?
        self.answer4 = Author.objects.filter(gender='ж').count()  # Сколько авторов женского пола зарегистрировано в системе?
        true_status_rule_authors = Author.objects.filter(status_rule='1').count()
        all_authors_count = Author.objects.count()
        self.answer5 = round(((100 * true_status_rule_authors) / all_authors_count), 2)  # Какой процент авторов согласился с правилами при регистрации?
        authors_stage_range = AuthorProfile.objects.filter(stage__gte=1).filter(stage__lte=5).values_list("author__id")
        self.answer6 = Author.objects.filter(id__in=authors_stage_range)  # Какие авторы имеют стаж от 1 до 5 лет?
        # self.answer6 = Author.objects.filter(authorprofile__stage__range=(1, 5))

        max_age_author = Author.objects.aggregate(max_age_author=Max('age'))
        self.answer7 = Author.objects.get(age=max_age_author['max_age_author'])  # Какой автор имеет наибольший возраст?
        self.answer8 = Author.objects.filter(phone_number__isnull=False).count()  # Сколько авторов указали свой номер телефона?
        self.answer9 = Author.objects.filter(age__lt=25)  # Какие авторы имеют возраст младше 25 лет?
        self.answer10 = Author.objects.annotate(count=Count('entries')).values('username', 'count')  # Сколько статей написано каждым автором?

        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}  # Создайте здесь запросы к БД

        return render(request, 'train_db/training_db.html', context=context)

