# polls/views.py
from django.shortcuts import render, redirect,get_object_or_404
from .models import Question, Choice


def index(request):
    all_questions = Question.objects.all()
    context = {'latest_question_list': all_questions}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:results', question_id=question.id)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})
def manual_entry(request):
    if request.method == 'POST':
        # Get data from the form
        question_text = request.POST.get('question_text')
        choices = [
            request.POST.get('choice1'),
            request.POST.get('choice2'),
            request.POST.get('choice3')
        ]

        # Create a new question
        question = Question(question_text=question_text)
        question.save()

        # Create choices for the question
        for choice_text in choices:
            if choice_text:
                choice = Choice(question=question, choice_text=choice_text)
                choice.save()

        return redirect('polls:index')  # Redirect to the index page

    return render(request, 'polls/manual_entry.html')


