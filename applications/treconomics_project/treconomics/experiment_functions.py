__author__ = 'leif'

import datetime
import logging
import logging.config
import logging.handlers

from django.contrib.auth.models import User
from models import DocumentsExamined
from experiment_configuration import timeout, rotations, event_logger, qrels_file
from experiment_configuration import exp_work_flows


def get_experiment_context(request):
    ec = {}
    ec["username"] = request.user.username
    u = User.objects.get( username=ec["username"] )
    profile = u.get_profile()
    ec["rotation"] = profile.rotation
    ec["condition"] = profile.condition
    ec["completed_steps"] = profile.steps_completed
    ec["workflow"] = exp_work_flows[profile.experiment]

    print ec["workflow"]
    if profile.data == "test":
        ec["test_user"] = True
    else:
        ec["test_user"] = False

    print "com_step: " + str(profile.steps_completed)

    if "current_step" in request.session:
        ec["current_step"] = request.session['current_step']
    else:
        # in the profile steps_completed is zero.
        #if the user logs in again, then if the session variable is not set, we take the one from the datbase
        steps_completed = ec["completed_steps"]
        ec["current_step"] = steps_completed
        request.session['current_step'] = steps_completed
        #request.session['current_url'] = ec["workflow"][steps_completed]

    if "taskid" in request.session:
        ec["taskid"] = int(request.session['taskid'])
        t = ec["taskid"] - 1
        r = ec["rotation"] - 1
        if t >= 0:
            ec["topicnum"] = rotations[r][t]
        else:
            ec["topicnum"] = 0
    else:
        ec["taskid"] = 0
        request.session["taskid"] = 0
        ec["topicnum"] = 0

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
    if ec["test_user"]:
        return False
    else:
        current_time = datetime.datetime.now()
        print current_time
        print start_time
        datetime.timedelta(0, 2700)

        diff = (current_time - start_time )
        d = diff.total_seconds()
        if d > timeout:
            return True
        else:
            return False

def log_event(event, request, query="", docid=-2, judgement=-2, docnum="", rank=-2, page=-2):
    ec = get_experiment_context(request)

    msg = ec["username"] + " " +  str(ec["condition"]) + " " + str(ec["taskid"]) + " " + str(ec["topicnum"]) + " "+  event;
    if docid > -1:
         event_logger.info( msg + " " + str(docid) + " " + docnum + " " + str(judgement) + " " + str(rank) )
    else:
        if page > 0:
            event_logger.info( msg + " " + str(page) )
        else:
            event_logger.info( msg + " " + query )

def mark_document(request, docid, judgement, title="", docnum="", rank=0):
    ec = get_experiment_context(request)
    username = ec["username"]
    task = ec["taskid"]
    topicnum = ec["topicnum"]
    if judgement == 1:
        #write_to_log("DOC_MARKED_RELEVANT", docid )
        log_event(event="DOC_MARKED_RELEVANT", request=request, docid=docid, judgement=1, docnum=docnum, rank=rank)
        print "DOC_MARKED_RELEVANT " + str(docid) + " " + docnum +  " " +  str(rank)
    if judgement == 0:
        #write_to_log("DOC_MARKED_NONRELEVANT", docid )
        print "DOC_MARKED_NONRELEVANT " + str(docid) + " " + docnum +  " " +  str(rank)
        log_event(event="DOC_MARKED_NONRELEVANT", request=request, docid=docid, judgement=0, docnum=docnum, rank=rank)
    if judgement < 0:
        # write_to_log("DOC_VIEWED"), docid )
        log_event(event="DOC_MARKED_VIEWED",docid=docid, request=request, docnum=docnum, rank=rank)
        print "DOC_VIEWED " + str(docid) + " " + docnum +  " " + str(rank)

    # check if user has marked the document or not
    u = User.objects.get(username=username)
    try:
        doc = DocumentsExamined.objects.filter(user=u).filter(task=task).get(docid=docid)
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
            doc = DocumentsExamined(user=u, title=title, docid=docid, url='/treconomics/'+docid+'/', task=task, topic_num=topicnum, doc_num=docnum, judgement=judgement, judgement_date=datetime.datetime.now())
            doc.save()

    return judgement


class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def ReadQrelsFile(qrel_file):
    qrels = AutoVivification()

    infile = open( qrel_file, "r" )
    while infile:
        line = infile.readline()
        parts = line.partition(' ')
        query_num = parts[0]
        parts = parts[2].partition(' ')
        parts = parts[2].partition(' ')
        doc_num = parts[0]
        judgement = parts[2].strip()

        qrels[query_num][doc_num] =  judgement

        if not line:
            break

    return qrels

def assessPerformance(qrels, topic_num, doc_list ):
    rels_found = 0
    non_rels_found = 0

    total = len(doc_list)
    for doc in doc_list:
        if qrels[topic_num][doc]:
            if int(qrels[topic_num][doc]) >= 1:
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


def getPerformance(qrels, username, taskid, rotation):
    topic_num = rotations[rotation-1][taskid-1]
    u = User.objects.get(username=username)
    docs = DocumentsExamined.objects.filter(user=u).filter(topic_num=topic_num)
    print docs
    doc_list = []
    for d in docs:
        if d.judgement > 0:
            doc_list.append(d.doc_num)
            print str(d.topic_num) + " " + d.doc_num

    return assessPerformance(qrels, str(topic_num), doc_list)


