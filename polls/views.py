from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from .models import Question , Choice

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
    	'latest_question_list' : latest_question_list
    }
    return render(request , "polls/index.html" , context)

def detail(request , question_id):
	question = get_object_or_404(Question , pk=question_id)
	context = {
		'question'	:	question
	}
	return render(request , "polls/details.html" , context)

def results(request , question_id):
    q = get_object_or_404(Question , pk=question_id)
    context = {
        'question': q
    }
    return render(request , 'polls/results.html' , context)

def vote(request , question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        context = {
            'question': q,
            'error_message': "You didn't select a choice."
        }
        return render(request , 'polls/details.html' , context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))

