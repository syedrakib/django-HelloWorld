from django.shortcuts import render , get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Question , Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    # Our polls/index.html template file uses "latest_question_list" as the context variable name 
    # instead of using "question_list" which would normally be the automatically generated
    # context variable name by a ListView.
    # ---
    # Hence, we must explicitly declare the context variable name 
    # which is being expected by the template file
    context_object_name = "latest_question_list"
    # Generic Views (ListView/DetailView etc) usually require declaring the model which should be used.
    # However, declaring a get_queryset() method won't require explicitly declaring the model again.
    def get_queryset(self):
        """Return the last 5 published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

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

