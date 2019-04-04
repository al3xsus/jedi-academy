from django.core.mail import send_mail
from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from jedi_academy.settings import EMAIL_MAIN
from .models import Jedi, Candidate, Trial, Answers, Students


class IndexView(TemplateView):

    template_name = "index.html"


class CandidateForm(ModelForm):

    class Meta:
        model = Candidate
        fields = ['name', 'planet', 'age', 'email']


class AnswersForm(ModelForm):

    class Meta:
        model = Answers
        fields = ['answer1', 'answer2', 'answer3']


def candidate_create(request, template_name='candidate.html'):
    form = CandidateForm(request.POST or None)
    if form.is_valid():
        try:
            new_candidate = form.save()
            return redirect("/candidate/{0}".format(new_candidate.pk))
        except:
            return render(request, 'error.html', {'text': 'Не удалось создать кандидата', 'code': 500})
    return render(request, template_name, {'form': form})


def candidate_testing(request, pk, template_name='candidate_test.html'):
    form = AnswersForm(request.POST or None)
    if not Candidate.objects.filter(pk=pk).exists():
        return render(request, 'error.html', {'text': 'Нет кандидата с id {}'.format(pk), 'code': 500})
    candidate = Candidate.objects.get(pk=pk)
    testing = list(Trial.objects.all())
    if not testing:
        return render(request, 'error.html', {'text': 'Нет теста для кандидата', 'code': 500})
    # testing = get_list_or_404(Trial)
    testing = testing[0]
    data = {'candidate': candidate, 'testing': testing, 'form': form}
    if form.is_valid():
        try:
            answers_new_instance = Answers(candidate_id=pk, trial_id=testing.pk, **form.cleaned_data)
            answers_new_instance.save()
        except:
            return render(request, 'error.html', {'text': 'Не удалось создать объект Answers', 'code': 500})
        finally:
            return redirect('index')
    return render(request, template_name, data)


class JediForm(ModelForm):

    class Meta:
        model = Jedi
        fields = ['name', 'planet']


class StudentsForm(ModelForm):

    class Meta:
        model = Students
        fields = ['padawans']


def jedi_list(request, filter_param=None, template_name='jedi.html'):
    if filter_param is not None:
        if filter_param.isnumeric():
            return jedi_choose_padawan(request, filter_param)
        else:
            if filter_param != 'all' and filter_param != 'manypad':
                return render(request, 'error.html', {'text': 'Некорректные параметры в строке запроса', 'code': 400})
    jedi_list_raw = list(Jedi.objects.all())
    if not jedi_list_raw:
        return render(request, 'error.html', {'text': 'Нет джедаев', 'code': 500})
    object_list = []
    for jedi in jedi_list_raw:
        if Students.objects.filter(jedi_id=jedi.pk).exists():
            students = Students.objects.get(jedi_id=jedi.pk)
            object_list.append({'name': jedi.name, 'planet': jedi.planet, 'pk': jedi.pk, 'padawans_count': students.padawans.count()})
        else:
            object_list.append({'name': jedi.name, 'planet': jedi.planet, 'pk': jedi.pk, 'padawans_count': 0})
    if filter_param is not None and filter_param == 'manypad':
        object_list_updated = []
        for obj in object_list:
            if obj['padawans_count'] > 1:
                object_list_updated.append(obj)
        object_list = object_list_updated
    data = {'object_list': object_list}
    return render(request, template_name, data)


def jedi_choose_padawan(request, pk, template_name='jedi_padawan.html'):
    if not Jedi.objects.filter(pk=pk).exists():
        return render(request, 'error.html', {'text': 'Нет джедая с id {}'.format(pk), 'code': 500})
    jedi = Jedi.objects.get(pk=pk)
    candidates = list(Candidate.objects.filter(planet=jedi.planet))
    if not candidates:
        return render(request, 'error.html', {'text': 'Нет кандидатов для такой планеты', 'code': 500})
    padawans_updated = []
    if Students.objects.filter(jedi_id=jedi.pk).exists():
        padawans = Students.objects.get(jedi_id=jedi.pk)
        for padawan in padawans.padawans.all():
            padawans_updated.append(padawan.name)
    candidates_updated = []
    buff = {}
    for candidate in candidates:
        buff['candidate'] = candidate
        buff['answers'] = get_object_or_404(Answers, candidate_id=candidate.pk)
        buff['questions'] = get_object_or_404(Trial, pk=buff['answers'].trial_id)
        candidates_updated.append(buff)
        buff = {}
    data = {'jedi': jedi, 'candidates': candidates_updated, 'padawans': padawans_updated}
    return render(request, template_name, data)


def padawan_changing(request, pk_jedi, pk_padawan):
    if not Jedi.objects.filter(pk=pk_jedi).exists():
        return render(request, 'error.html', {'text': 'Нет джедая с id {}'.format(pk_jedi), 'code': 500})
    jedi = Jedi.objects.get(pk=pk_jedi)
    if not Candidate.objects.filter(pk=pk_padawan).exists():
        return render(request, 'error.html', {'text': 'Нет кандидата с id {}'.format(pk_jedi), 'code': 500})
    candidate = Candidate.objects.get(pk=pk_padawan)
    try:
        if Students.objects.filter(jedi_id=pk_jedi).exists():
            future_jedi = Students.objects.get(jedi_id=pk_jedi)
            if candidate in future_jedi.padawans.all():
                future_jedi.padawans.remove(candidate)
            else:
                if future_jedi.padawans.count() < 3:
                    future_jedi.padawans.add(candidate)
                    send_mail(
                        'Зачисление в падаваны',
                        'Поздравляем, {}! Джедай {} готов принять Вас в падаваны.'.format(candidate.name, jedi.name),
                        EMAIL_MAIN,
                        [candidate.email],
                        fail_silently=False,
                    )
                else:
                    pass
        else:
            future_jedi = Students(jedi_id=pk_jedi)
            future_jedi.save()
            future_jedi.padawans.add(candidate)
            send_mail(
                'Зачисление в падаваны',
                'Поздравляем, {}! Джедай {} готов принять Вас в падаваны.'.format(candidate.name, jedi.name),
                EMAIL_MAIN,
                [candidate.email],
                fail_silently=False,
            )
        future_jedi.save()
    except:
        return render(request, 'error.html', {'text': 'Не удалось изменить падаванов', 'code': 500})
    finally:
        return redirect("/jedi/{0}".format(pk_jedi))
