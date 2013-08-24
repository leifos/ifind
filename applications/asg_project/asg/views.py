# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from ifind.search.cache import RedisConn
from ifind.asg.abstract_search_game import ABSGame
from ifind.asg.asg_generator import RandomYieldGenerator, CueGenerator

ryg = RandomYieldGenerator()
cg = CueGenerator()


def index(request):
        context = RequestContext(request, {})
        return render_to_response('asg/game.html', context)

def startgame(request):
        context = RequestContext(request, {})
        rc = RedisConn()
        rc.connect()
        rc.store('test','start was pressed')

        game = ABSGame(ryg,cg)

        game.start_game()
        data = game.get_game_state()
        rc.store('game',game)
        return render_to_response('asg/game.html', {'v':'Game Started', 'data': data }, context)


def query(request):
        context = RequestContext(request, {})
        rc = RedisConn()
        rc.connect()
        v = rc.get('test')
        if v:
            game = rc.get('game')
            game.issue_query()
            v = game.tokens
            rc.store('game',game)
            data = game.get_game_state()
        return render_to_response('asg/game.html', {'v': v, 'data': data}, context)

def assess(request):
        context = RequestContext(request, {})
        rc = RedisConn()
        rc.connect()
        v = rc.get('test')
        if v:
            game = rc.get('game')
            game.examine_document()
            v = game.tokens
            rc.store('game',game)
            data = game.get_game_state()
        rc.store('test','assessed was pressed')
        return render_to_response('asg/game.html', {'v': v, 'data': data}, context)