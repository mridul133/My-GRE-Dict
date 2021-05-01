from django.shortcuts import render
from django.http import HttpResponse
from pages.models import *
from django.contrib import messages 
from django.db.models import F
import random
import json
import os


MX_WEIGHT = 100.0

def home_view(request, *args, **kwargs):

    prev_word = update_info_about_prev_word(request)
    next_word = get_next_word(request, prev_word)

    ret = get_return_object(next_word)

    return render(request, "home.html", ret)

def manage_view(request, *args, **kwargs):
    return render(request, "manage.html", {})



#==================================== Helper Functions ===================================


def update_info_about_prev_word(request):

    if('word' not in request.POST):
        return ""
    
    prev_word = request.POST['word']
    prev_word_weight = float(request.POST['weight'])
    
    is_sort_order_alpha = 0

    if('sort_order' in request.POST):
        if(request.POST['sort_order'] == "on"):
            is_sort_order_alpha = 1
        else:
            is_sort_order_alpha = 0
    else:
        is_sort_order_alpha = 0
        

    Global.objects.all().update(AlphaSort = is_sort_order_alpha)
    Global.objects.all().update(TotalWords = len(Word.objects.all()))

    Word.objects.filter(Weight__gt = MX_WEIGHT/5.0).update(Weight = F("Weight") + 1)
    Word.objects.filter(Weight__lte = MX_WEIGHT/5.0).update(Weight = F("Weight") + 0.3)
    Word.objects.filter(Weight__gt = MX_WEIGHT).update(Weight = MX_WEIGHT)

    db_entry =  Word.objects.filter(Word = prev_word)

    if(len(db_entry) == 0):
        return ""

    db_entry[0].AppearCnt += 1

    if(abs(prev_word_weight-db_entry[0].Weight) >= 1.0):
        db_entry[0].Weight = prev_word_weight
    db_entry[0].save()

    Global.objects.all().update(MasteredCnt = len(Word.objects.filter(Weight__lte = MX_WEIGHT/5.0)))
    
    return prev_word


def get_next_word(request, prev_word):

    isSearched = 0
    if('search' in request.GET):
        isSearched = 1
        prev_word = request.GET['search']
    
    all_words = Word.objects.all()

    if(len(Global.objects.all()) == 0):
        Global.objects.create(TotalWords = len(all_words), MasteredCnt = 0, AlphaSort = 0)

    if(len(all_words) == 0):
        ret = ["No word in the database", "", "", "", 0.0, 0]
        return ret

    if(len(all_words) > 1):
        if(isSearched == 1):
            all_words = all_words.filter(Word = prev_word)
        else:
            all_words = all_words.exclude(Word = prev_word)

    words = []

    for word in all_words:
        words.append([word.Word, word.POS, word.Definition, word.Example, word.Weight, word.AppearCnt])

    if(len(Global.objects.filter(AlphaSort = 1)) > 0):
        return get_next_word_in_alphabatical_order(words)
    
    return get_next_high_weight_random_word(words)


def get_next_word_in_alphabatical_order(words):

    words.sort(key=lambda tup: tup[0])
    ind = 0
    while(ind < len(words)):
        if(words[ind][4] > MX_WEIGHT/5.0):
            break
        ind += 1
    if(ind >= len(words)):
        ind -= 1

    return words[ind]

def get_next_high_weight_random_word(words):
    
    words.sort(key=lambda tup: tup[4], reverse=True)

    top_words = []
    for i in range(0, len(words)):
        if(words[i][4] == words[0][4]):
            top_words.append(words[i])

    random.shuffle(top_words)

    return top_words[0]


def get_return_object(next_word):

    global_var = Global.objects.all()
    all_words = Word.objects.all()
    
    words = []
    for word in all_words:
        words.append(str(word.Word))

    json_words = json.dumps(words)

    ret = {}

    ret['word'] = next_word[0]
    ret['pos'] = "("+next_word[1]+")"
    ret['def'] = next_word[2]
    ret['exm'] = next_word[3]
    ret['weight'] = next_word[4]
    ret['cnt'] = next_word[5]
    ret['alpha_sort'] = global_var[0].AlphaSort
    ret['mastered'] = global_var[0].MasteredCnt
    ret['total'] = global_var[0].TotalWords
    ret['all_words'] = json_words
    ret['mx_weight'] = MX_WEIGHT

    return ret




def add_new_word(request):

    word = fix_lower_upper(request.POST['new_word'])
    pos = fix_lower_upper(request.POST['new_word_pos'])
    definition = fix_lower_upper(request.POST['new_word_def'])
    example = fix_lower_upper(request.POST['new_word_example'])
    
    Word.objects.create(Word = word, POS = pos, Definition = definition, Example = example, Weight = MX_WEIGHT, AppearCnt = 0)

    messages.success(request, "New word added !")

    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")


def delete_word():
    print("deleted")


def initialize_db_with_magoosh1000(request):
    
    Word.objects.all().delete()

    data = []
    with open(os.path.dirname(os.path.realpath(__file__)) + '/magoosh1000.json') as f:
        data = json.load(f)

    for curr in data:

        curr['word'] = fix_lower_upper(curr['word'])
        curr['pos'] = fix_lower_upper(curr['pos'])
        curr['definition'] = fix_lower_upper(curr['definition'])
        curr['example'] = fix_lower_upper(curr['example'])

        Word.objects.create(Word = curr['word'], POS = curr['pos'], Definition = curr['definition'], Example = curr['example'], Weight = MX_WEIGHT, AppearCnt = 0)

    messages.success(request, "Initialization successfull !")

    return HttpResponse("""<html><script>window.location.replace('/manage');</script></html>""")


def reset_all_weights_to_max(request):
    
    all_words = Word.objects.all()

    for word in all_words:
        word.Weight = MX_WEIGHT
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