from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login, logout


from .forms import ContactoForm, RegistroForm, UsuarioLoginForm, PreguntasRespondidas
from .models import QuizUsuario, Pregunta


def comment(request):
    print(request.method, 'comment')
    return render(request, 'api/comment.html')


def quiz(request):
    print(request.method, 'quiz')
    return render(request, 'quiz/play.html')


def contact(request, send=True):
    print(request.method, 'contact')
    return render(request, 'api/contact.html', {'form': ContactoForm()})


def user(request):
    #Temporary
    return render(request, 'api/user.html')


api_views = [contact, quiz, comment]


def user_logout(request):
    logout(request)
    return redirect('/')


def user_login(request):
    title = 'login'
    form = UsuarioLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/?section=1")

    context = {
        'form': form,
        'title': title,
    }

    return render(request, 'user/login.html', context)


def user_register(request):
    title = 'Crear una Cuenta'

    if request.method == "POST":
        form = RegistroForm(data=request.POST)
        if form.is_valid():
            form.save()
            print("Enhorabuena El registro ha ido bien.")
            return redirect('/user/login')
        print("Erro al registar el nuevo usuario.")
    else:
        form = RegistroForm()

    context = {
        'form': form,
        'title': title
    }
    return render(request, 'user/register.html', context)


def quiz_play(request):
    QuizUser, created = QuizUsuario.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        question_pk = request.POST.get('question_pk')
        question_answered = QuizUser.attempts.select_related('question').get(question__pk=question_pk)
        answer_pk = request.POST.get('question_pk')
        try:
            selected_option = question_answered.question.options.get(pk=answer_pk)
        except ObjectDoesNotExist:
            raise Http404
        QuizUser.validate_attempt(question_answered, selected_option)

        return redirect(f"/quiz/result/{question_answered.pk}")
    else:
        question = QuizUser.get_new_questions()
        if question is not None:
            QuizUser.create_attempts(question)
        context = {
            'question': question

        }
    return render(request, 'quiz/play.html', context)


def quiz_result(request, question_answered_pk):
    answered = get_object_or_404(PreguntasRespondidas, pk=question_answered_pk)
    context = {
        'answered': answered,
    }
    return render(request, "quiz/result.html", context)


def section(request, num):
    print(request.method, 'section')
    if request.method == "POST":
        if 1 <= len(api_views) >= num:
            return api_views[num - 1](request)
        else:
            raise Http404("No such section")
    else:
        raise Http404("No method GET")


def index(request):
    my_forms = { 'contact': ContactoForm }
    num = int(request.GET.get("section", 2))
    send = request.GET.get("send", False)
    # Si no obter el GET ?section=num, entonces por default tenemos el quiz, num = 2.
    print(str(request.user), 'index')

    if request.user.is_authenticated:
        print(request.user, "login success!")

    if request.method == 'POST' and send:
        form = my_forms[send](data=request.POST)
        if form.is_valid():
            form.save()

    print(str(request.user))

    if str(request.user) != "AnonymousUser":
        return render(request, 'website/index.html', {'section': num})
    else:
        return redirect('user/login')
