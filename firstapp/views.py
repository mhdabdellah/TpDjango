from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.urls import reverse
from .models import Question,Choice
from django.utils import timezone
from django.views import generic


def index1(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def index2(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('firstapp/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'firstapp/index.html', context)


def detail1(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results1(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote1(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def detail2(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'firstapp/detail.html', {'question': question})

# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'firstapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('firstapp:results', args=(question.id,)))
    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'firstapp/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'firstapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView1(generic.DetailView):
    model = Question
    template_name = 'firstapp/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'firstapp/results.html'



class IndexView(generic.ListView):
    template_name = 'firstapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
    

def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    ...
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())