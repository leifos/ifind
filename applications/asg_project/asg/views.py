# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from ifind.search.cache import RedisConn
from ifind.asg.abstract_search_game import ABSGame
from ifind.asg.asg_generator import RandomYieldGenerator, ConstantLinearYieldGenerator, TestYieldGenerator, CueGenerator

ryg = RandomYieldGenerator()
tyg = TestYieldGenerator()
cyg = ConstantLinearYieldGenerator()
cg = CueGenerator(cue_length=30)


def index(request):
        context = RequestContext(request, {})
        return render_to_response('asg/game.html', context)

def startgame(request):
        context = RequestContext(request, {})
        request.session.flush()
        session_id = request.session._get_or_create_session_key()
        print session_id
        rc = RedisConn()
        rc.connect()
        game = ABSGame(ryg,cg,cq=2)
        game.start_game()
        data = game.get_game_state()
        rc.store(session_id, game)
        response = render_to_response('asg/game.html', {'sid':session_id, 'data': data }, context)
        response.set_cookie('gid',session_id)
        return response

def startgame2(request):
        context = RequestContext(request, {})
        request.session.flush()
        session_id = request.session._get_or_create_session_key()
        print session_id
        rc = RedisConn()
        rc.connect()
        game = ABSGame(tyg,cg,cq=2)
        game.start_game()
        data = game.get_game_state()
        rc.store(session_id, game)
        response = render_to_response('asg/game.html', {'sid':session_id, 'data': data }, context)
        response.set_cookie('gid',session_id)
        return response


def query(request):
        context = RequestContext(request, {})

        gid = ''
        if request.COOKIES.has_key('gid'):
            gid = request.COOKIES['gid']
        rc = RedisConn()
        rc.connect()
        game = rc.get(gid)
        if game:
            game.issue_query()
            rc.store(gid,game)
            data = game.get_game_state()

        return render_to_response('asg/game.html', {'sid':gid, 'data': data}, context)

def assess(request):
        context = RequestContext(request, {})
        rc = RedisConn()
        rc.connect()
        gid = ''
        if request.COOKIES.has_key('gid'):
            gid = request.COOKIES['gid']

        data = {}
        game = rc.get(gid)
        if game:
            game.examine_document()
            rc.store(gid,game)
            data = game.get_game_state()
        return render_to_response('asg/game.html', {'sid':gid, 'data': data}, context)