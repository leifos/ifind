__author__ = 'leif'

import datetime
import logging
import logging.config
import logging.handlers
from ifind.seeker.trec_qrel_handler import TrecQrelHandler


from django.contrib.auth.models import User
from models import DocumentsExamined
from experiment_configuration import event_logger, qrels_file
from experiment_configuration import experiment_setups
from pytz import timezone
from django.conf import settings

settings_timezone = timezone(settings.TIME_ZONE)
qrels = TrecQrelHandler(qrels_file)


def get_experiment_context(request):
    ec = {}
    ec["username"] = request.user.username
    u = User.objects.get( username=ec["username"] )
    profile = u.get_profile()
    ec["rotation"] = profile.rotation
    ec["condition"] = profile.condition
    ec["completed_steps"] = profile.steps_completed
    ec["workflow"] = experiment_setups[ec['condition']].workflow

    if profile.data == "test":
        ec["test_user"] = True
    else:
        ec["test_user"] = False

    if "current_step" in request.session:
        ec["current_step"] = int(request.session['current_step'])
    else:
        # in the profile steps_completed is zero.
        #if the user logs in again, then if the session variable is not set, we take the one from the datbase
        steps_completed = ec["completed_steps"]
        ec["current_step"] = steps_completed
        request.session['current_step'] = steps_completed

    if "taskid" in request.session:
        ec["taskid"] = int(request.session['taskid'])
        t = ec["taskid"] - 1
        r = ec["rotation"] - 1
        if t >= 0:
            ec["topicnum"] = experiment_setups[ec['condition']].get_rotation_topic(r, t)
        else:
            ec["topicnum"] = experiment_setups[ec['condition']].practice_topic
    else:
        ec["taskid"] = 0
        request.session["taskid"] = 0
        ec["topicnum"] = experiment_setups[ec['condition']].practice_topic

    return ec

def print_experiment_context(ec):
    print "username: " + ec["username"]
    print "rotation: " + str(ec["rotation"])
    print "condition: " + str(ec["condition"])
    print "completed steps: " + str(ec["completed_steps"])
    print "current step: " + str(ec["current_step"])
    print "taskid: " + str(ec["taskid"])
    print "topicnum: " + str(ec["topicnum"])


def time_search_experiment_out(request):
    start_time = request.session['start_time']
    ec = get_experiment_context(request)
    timeout = experiment_setups[ec['condition']].timeout

    if ec["test_user"]:
        return False
    else:
        current_time = datetime.datetime.now()
        start_time_obj = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        datetime.timedelta(0, 2700)

        diff = (current_time - start_time_obj)
        d = diff.total_seconds()
        if d > timeout:
            return True
        else:
            return False

def log_event(event, request, query="", whooshid=-2, judgement=-2, trecid="", rank=-2, page=-2, doc_length=0):
    ec = get_experiment_context(request)

    msg = ec["username"] + " " + str(ec["condition"]) + " " + str(ec["taskid"]) + " " + str(ec["topicnum"]) + " " + event

    if whooshid > -1:
        event_logger.info(msg + " " + str(whooshid) + " " + trecid + " " + str(doc_length) + " " + str(judgement) + " " + str(rank))
    else:
        if page > 0:
            event_logger.info(msg + " " + str(page))
        else:
            event_logger.info(msg + " " + query)

def mark_document(request, whooshid, judgement, title="", trecid="", rank=0, doc_length=-1):
    ec = get_experiment_context(request)
    username = ec["username"]
    task = ec["taskid"]
    topicnum = ec["topicnum"]

    if judgement == 1:
        #write_to_log("DOC_MARKED_RELEVANT", whooshid )
        log_event(event="DOC_MARKED_RELEVANT", request=request, whooshid=whooshid, judgement=1, trecid=trecid, rank=rank, doc_length=doc_length)
        print "DOC_MARKED_RELEVANT " + str(whooshid) + " " + trecid + " " + str(rank)
    if judgement == 0:
        #write_to_log("DOC_MARKED_NONRELEVANT", whooshid )
        print "DOC_MARKED_NONRELEVANT " + str(whooshid) + " " + trecid + " " + str(rank)
        log_event(event="DOC_MARKED_NONRELEVANT", request=request, whooshid=whooshid, judgement=0, trecid=trecid, rank=rank, doc_length=doc_length)
    if judgement < 0:
        # write_to_log("DOC_VIEWED"), whooshid )
        log_event(event="DOC_MARKED_VIEWED", whooshid=whooshid, request=request, trecid=trecid, rank=rank, doc_length=doc_length)
        print "DOC_VIEWED " + str(whooshid) + " " + trecid + " " + str(rank)

    # check if user has marked the document or not
    u = User.objects.get(username=username)
    try:
        doc = DocumentsExamined.objects.filter(user=u).filter(task=task).get(docid=whooshid)
        if doc:
            # update judgement that is already there
            if judgement > -1:
                print "doc judge changed to: " + str(judgement) + " from: " + str(doc.judgement)
                doc.judgement = judgement
                doc.save()
            else:
                judgement = doc.judgement

    except DocumentsExamined.DoesNotExist:
        # create an entry to show the document has been judged
#        print "no doc found in db"
        if judgement > -1:
            print "doc judge set to: " + str(judgement)
            doc = DocumentsExamined(user=u, title=title, docid=whooshid, url='/treconomics/'+whooshid+'/', task=task, topic_num=topicnum, doc_num=trecid, judgement=judgement, judgement_date=datetime.datetime.now(tz=settings_timezone))
            doc.save()

    return judgement


def assessPerformance(topic_num, doc_list):
    rels_found = 0
    non_rels_found = 0

    total = len(doc_list)
    for doc in doc_list:
        val = qrels.get_value(topic_num, doc)
        if val:
            if int(val) >= 1:
                rels_found = rels_found + 1
            else:
                non_rels_found = non_rels_found + 1
        else:
            non_rels_found = non_rels_found + 1

    performance = {}
    performance['topicnum'] = topic_num
    performance['rels'] = rels_found
    performance['nons'] = non_rels_found
    return performance


def getPerformance(username, topic_num):
    u = User.objects.get(username=username)
    docs = DocumentsExamined.objects.filter(user=u).filter(topic_num=topic_num)
    print "Documents to Judge for topic %s " % (topic_num)
    doc_list = []
    for d in docs:
        if d.judgement > 0:
            doc_list.append(d.doc_num)
            print str(d.topic_num) + " " + d.doc_num

    return assessPerformance(str(topic_num), doc_list)


def getQueryResultPerformance(results, topic_num):

    i = 0
    rels_found = 0
    for r in results:
        i = i + 1
        val = qrels.get_value(topic_num, r.docid)
        if val > 0:
            rels_found = rels_found + 1


    return [rels_found, i]
