from django.shortcuts import render
from django.http import HttpResponse
import json
import os
from pages.models import Word
from pages.models import Global
from django.contrib import messages 
import random


# Create your views here.

def home_view(request, *args, **kwargs):

    if('word' in request.POST):
        update_info_about_old_word(request)
    
    word = get_random_word()

    global_var = Global.objects.all()
    
    ret = {}

    ret['word'] = word[0]
    ret['pos'] = "("+word[1]+")"
    ret['def'] = word[2]
    ret['exm'] = word[3]
    ret['weight'] = word[4]
    ret['cnt'] = word[5]
    ret['alpha_sort'] = global_var[0].AlphaSort
    ret['mastered'] = global_var[0].MasteredCnt
    ret['total'] = global_var[0].TotalWords

    print("ret ----- >", ret)

    return render(request, "home.html", ret)

def manage_view(request, *args, **kwargs):
    return render(request, "manage.html", {})



#==================================== Helper Functions ===================================

def add_new_word(request):

    word = fix_lower_upper(request.POST['new_word'])
    pos = fix_lower_upper(request.POST['new_word_pos'])
    definition = fix_lower_upper(request.POST['new_word_def'])
    example = fix_lower_upper(request.POST['new_word_example'])
    
    Word.objects.create(Word = word, POS = pos, Definition = definition, Example = example, Weight = 100.0, AppearCnt = 0)

    messages.success(request, "New word added !")

    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")


def delete_word():
    print("deleted")

def initialize_db_with_magoosh1000(request):
    
    Word.objects.all().delete()

    data = []
    with open(os.path.dirname(os.path.realpath(__file__)) + '/magoosh1000.json') as f:
        data = json.load(f)

    cnt = 0
    for curr in data:
        cnt += 1

        curr['word'] = fix_lower_upper(curr['word'])
        curr['pos'] = fix_lower_upper(curr['pos'])
        curr['definition'] = fix_lower_upper(curr['definition'])
        curr['example'] = fix_lower_upper(curr['example'])

        Word.objects.create(Word = curr['word'], POS = curr['pos'], Definition = curr['definition'], Example = curr['example'], Weight = 100.0, AppearCnt = 0)

    messages.success(request, "Initialization successfull !")

    return HttpResponse("""<html><script>window.location.replace('/manage');</script></html>""")


def reset_all_weights_to_max(request):
    
    all_words = Word.objects.all()

    for word in all_words:
        word.Weight = 100.0
        word.save()
    
    messages.success(request, "Weights have been reset successfully !")

    return HttpResponse("""<html><script>window.location.replace('/manage');</script></html>""")


def refresh_words(request):

    all_words = Word.objects.all()

    for word in all_words:
        word.Word = fix_lower_upper(word.Word)
        word.POS = fix_lower_upper(word.POS)
        word.Definition = fix_lower_upper(word.Definition)
        word.Example = fix_lower_upper(word.Example)
        word.save()
    
    messages.success(request, "Words have been refreshed successfully !")

    return HttpResponse("""<html><script>window.location.replace('/manage');</script></html>""")


def clear_database(request):
    Word.objects.all().delete()
    Global.objects.all().delete()
    messages.success(request, "Database has been cleared successfully !")
    return HttpResponse("""<html><script>window.location.replace('/manage');</script></html>""")


def fix_lower_upper(s):

    if(len(s) == 0):
        return s

    chars = list(s)

    indexes = [0]

    s = s.lower()

    for i in range(0, len(s)-1):
        if(s[i] == '.'):
            j = i
            while(j < len(s)):
                if(s[j].isalpha()):
                    indexes.append(j)
                    break
                elif(s[j].isdigit()):
                    break
                j += 1

    for i in indexes:
        chars[i] = chars[i].upper()

    s = ''.join(chars)

    return s


def get_random_word():
    
    all_words = Word.objects.all()

    if(len(all_words) == 0):

        Global.objects.create(TotalWords = 0, MasteredCnt = 0, AlphaSort = 0)

        ret = ["No word in the database", "", "", "", 0.0, 0]
        return ret

    words = []

    for word in all_words:
        words.append([word.Word, word.POS, word.Definition, word.Example, word.Weight, word.AppearCnt])

    words.sort(key=lambda tup: tup[1], reverse=True)

    top10 = []
    for i in range(0, min(10, len(words))):
        top10.append(words[i])

    ret = top10[random.randint(0,len(top10)-1)]

    return ret

def update_info_about_old_word(request):

    old_word = request.POST['word']
    old_word_weight = request.POST['weight']
    
    check_box = 0

    if('sort_order' in request.POST):
        if(request.POST['sort_order'] == "on"):
            check_box = 1
        else:
            check_box = 0
    else:
        check_box = 0

    Global.objects.all().update(AlphaSort = check_box)

    if(old_word_weight == 0):
        print("ysssssssssssssssssssssssssssssssssssssssssssss")
        Global.objects.all().update(MasteredCnt = MasteredCnt + 1)

    Global.objects.all().update(TotalWords = len(Word.objects.all()))

    db_entry =  Word.objects.filter(Word = old_word)

    if(len(db_entry) == 0):
        return

    db_entry[0].AppearCnt += 1
    db_entry[0].Weight = old_word_weight
    db_entry[0].save()