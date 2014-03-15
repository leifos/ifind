__author__ = 'david'
import os
import sys

from ifind.seeker.trec_qrel_handler import TrecQrelHandler

def ratio(rels, nonrels):
    """ expect two floats
    """
    dem = rels + nonrels
    if dem > 0.0:
        return round((rels * rels) / dem, 2)
    else:
        return 0.0

def get_perf():
    OUT_FILE = 'user_perf.txt'
    out_f = open(OUT_FILE, 'w')

    qrels = TrecQrelHandler('data/TREC2005.qrels.txt')

    topics = [347, 435]

    #users = get_newssearch_users()
    users = UserProfile.objects.all()

    for user in users:
        username = user.user.username
        condition = user.condition

        for t in topics:
            examined_docs = DocumentsExamined.objects.filter(user=user.user, topic_num=t)
            total_docs = len(examined_docs)

            rel_correct = 0
            rel_incorrect = 0

            for doc in examined_docs:
                assessor_judgement = qrels.get_value(str(t), doc.doc_num)
                user_judgement = doc.judgement

                if assessor_judgement > 0:
                    assessor_judgement = True
                else:
                    assessor_judgement = False

                if user_judgement > 0:
                    user_judgement = True
                else:
                    user_judgement = False

                if assessor_judgement and user_judgement:
                    rel_correct = rel_correct + 1

                if not assessor_judgement and user_judgement:
                    rel_incorrect = rel_incorrect + 1

            out_f.write("{:<12}{:< 8}{:<8}{:<8}{:<8}{:10.2f}\n".format(
                username,
                t,  # (topic number)
                total_docs,  # (total number of docs marked)
                rel_correct,  # (number of documents marked which were correct)
                rel_incorrect,  # (number of documents marked incorrectly)
                ratio(float(rel_correct), rel_incorrect)  # (ratio between correct/incorrect)
            ))

    out_f.close()

def get_newssearch_users():
    profiles = UserProfile.objects.all()
    search = []
    excluded = ['search12', 'search13', 'search26', 'search27', 'search40', 'search41', 'search54', 'search55']

    for user in profiles:
        if user.user.username.startswith('search'):
            if user.user.username not in excluded:
                search.append(user)

    return search
    
    
    
    
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'treconomics_project.settings')
    from django.contrib.auth.models import User
    from treconomics.models import UserProfile, DocumentsExamined
    get_perf()
    