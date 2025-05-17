# from django.core.paginator import Paginator

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday
from .models import Congratulation
from .utils import calculate_birthday_countdown


@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)


class BirthdayListView(ListView):
    model = Birthday
    queryset = Birthday.objects.prefetch_related(
        'tags'
    ).select_related('author')
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(CreateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


# def birthday(request, pk=None):
#     template_name = 'birthday/birthday.html'

#     if pk is not None:
#         instance = get_object_or_404(Birthday, pk=pk)
#     else:
#         instance = None

#     form = BirthdayForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=instance)

#     context = {'form': form}

#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update(
#             {'birthday_countdown': birthday_countdown}
#         )

#     return render(request, template_name, context)

# instead of that we used class BirthdayListView(ListView)
# def birthday_list(request):
#     template = 'birthday/birthday_list.html'

#     birthdays = Birthday.objects.order_by('id')

#     paginator = Paginator(birthdays, 3)

#     page_number = request.GET.get('page')

#     page_obj = paginator.get_page(page_number)

#     # context = {'birthdays': birthdays}
#     context = {'page_obj': page_obj}

#     return render(request, template, context)


# def delete_birthday(request, pk):
#     template = 'birthday/birthday.html'

#     instance = get_object_or_404(Birthday, pk=pk)

#     form = BirthdayForm(instance=instance)

#     context = {'form': form}

#     if request.method == 'POST':
#         instance.delete()

#         return redirect('birthday:list')

#     return render(request, template, context)
