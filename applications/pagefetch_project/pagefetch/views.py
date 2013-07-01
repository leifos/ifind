# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext


def test(request):
    context = RequestContext(request)
    return render_to_response('pagefetch/test.html', {}, context)

def index(request):
    pass

def leaderboard(request):
    pass

def login():
    pass

def logout():
    pass

def start_game():
    pass

def choose_cat():
    pass

def end_game():
    pass

def perform_search():
    pass

def new_page():
    pass

def game_stats():
    pass

def quit_game():
    pass

def register(request):
    pass



