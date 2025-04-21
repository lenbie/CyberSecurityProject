from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.urls import reverse
from django.db import connection

from django.contrib.auth.decorators import login_required #ADD
from django.contrib.auth.models import User
from django.contrib import messages

## FIX FLAW 1 
#from django.contrib.auth.password_validation import validate_password
#from django.core.exceptions import ValidationError

from .models import Choice, Question

@login_required
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "polls/register.html", {"errors": ["This username already exists"]})

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")

    return render(request, "polls/register.html")

"""
FIX FLAW 1
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, "polls/register.html", {"errors": ["Invalid credentials. Check that the username is unique and password is strong, containing at least 8 characters and both numbers and letters."]})
        
        if User.objects.filter(username=username).exists():
            return render(request, "polls/register.html", {"errors": ["Invalid credentials. Check that the username is unique and password is strong, containing at least 8 characters and both numbers and letters."]})

        user = User.objects.create_user(username=username, password=password)
        return redirect("login")


    return render(request, "polls/register.html")
"""

# FIX FLAW 3 @login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

# FIX FLAW 3 @login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

# FIX FLAW 3 @login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

@login_required
def delete(request, question_id):

    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM polls_question WHERE id = {question_id}")

    return redirect("/")

"""
FIX FLAW 4

@login_required
def delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect("/")
"""