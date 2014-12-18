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
    u = User.objects.get(username=ec["username"])
    profile = u.get_profile()
    ec["rotation"] = profile.rotation
    ec["condition"] = profile.condition
    ec["completed_steps"] = profile.steps_completed
    ec["workflow"] = experiment_setups[ec['condition']].workflow

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

    if timeout == 0:
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


def log_performance(request, perf):
    ec = get_experiment_context(request)

    msg = ec["username"] + " " + str(ec["condition"]) + " 0 " + perf["num"] + " VIEW_PERFORMANCE "
    msg = msg + " " + str(perf["total"]) + " " + str(perf["score"]) + " " + str(perf["rels"]) + " " + str(perf["nons"])
    event_logger.info(msg)


def log_event(event, request, query="", whooshid=-2, judgement=-2, trecid="", rank=-2, page=-2, doc_length=0, metrics=None):
    ec = get_experiment_context(request)

    msg = ec["username"] + " " + str(ec["condition"]) + " " + str(ec["taskid"]) + " " + str(ec["topicnum"]) + " " + event

    if whooshid > -1:
        event_logger.info(msg + " " + str(whooshid) + " " + trecid + " " + str(doc_length) + " " + str(judgement) + " " + str(rank))
    else:
        if page > 0:
            event_logger.info(msg + " " + str(page))
        elif metrics:
            metrics_string = ""

            # The order in which metrics appear is determined by how they are returned in
            # experiment_functions.get_query_performance_metrics().
            for metric in metrics:
                if type(metric) == int:
                    metrics_string = metrics_string + " " + str(metric)
                else:
                    metrics_string = metrics_string + " " + ("%.4f" % metric)

            event_logger.info(msg + " '" + query + "'" + str(metrics_string))
        else:
            if query and rank > 0:
                event_logger.info(msg + " '" + query + "' " + str(rank))
            elif query:
                event_logger.info(msg + " '" + query + "'")
            else:
                event_logger.info(msg)


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
        # print "no doc found in db"
        if judgement > -1:
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

def get_topic_relevant_count(topic_num):
    """
    Returns the number of documents considered relevant for topic topic_num.
    """
    count = 0

    for document in qrels.get_doc_list(topic_num):
        if qrels.get_value(topic_num, document) > 0:
            count = count + 1

    return count

def calculate_precision(results, topic_num, k):
    """
    Returns a float representing the precision @ k for a given topic, topic_num, and set of results, results.
    """
    results = results[0:k]
    no_relevant = getQueryResultPerformance(results, topic_num)[0]
    return no_relevant / float(k)


def get_query_performance_metrics(results, topic_num):
    """
    Returns performance metrics for a given list of results, results, and a TREC topic, topic_num.
    List returned is in the format [p@1, p@2, p@3, p@4, p@5, p@10, p@15, p@20, p@125, p@30, p@40, p@50, Rprec, total rel. docs]
    """
    
    total_relevant_docs = get_topic_relevant_count(topic_num)

    p_at_1 = calculate_precision(results, topic_num, 1)
    p_at_2 = calculate_precision(results, topic_num, 2)
    p_at_3 = calculate_precision(results, topic_num, 3)
    p_at_4 = calculate_precision(results, topic_num, 5)
    p_at_5 = calculate_precision(results, topic_num, 6)
    p_at_10 = calculate_precision(results, topic_num, 10)
    p_at_15 = calculate_precision(results, topic_num, 15)
    p_at_20 = calculate_precision(results, topic_num, 20)
    p_at_25 = calculate_precision(results, topic_num, 25)
    p_at_30 = calculate_precision(results, topic_num, 30)
    p_at_40 = calculate_precision(results, topic_num, 40)
    p_at_50 = calculate_precision(results, topic_num, 50)
    r_prec = int(calculate_precision(results, topic_num, total_relevant_docs))

    return [p_at_1, p_at_2, p_at_3, p_at_4, p_at_5, p_at_10, p_at_15, p_at_20, p_at_25, p_at_30, p_at_40, p_at_50, r_prec, total_relevant_docs]