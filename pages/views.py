from django.shortcuts import render
from django.http import HttpResponse
import json
import os
from pages.models import Word
from django.contrib import messages 


# Create your views here.

def home_view(request, *args, **kwargs):
    print("---> 2 ---> ", request.POST)
    return render(request, "home.html", {})

def manage_view(request, *args, **kwargs):
    return render(request, "manage.html", {})



#==================================== Helper Functions ===================================

def add_new_word(request):

    word = fix_lower_upper(request.POST['new_word'])
    pos = fix_lower_upper(request.POST['new_word_pos'])
    definition = fix_lower_upper(request.POST['new_word_def'])
    example = fix_lower_upper(request.POST['new_word_example'])
    
    Word.objects.create(Word = word, POS = pos, Definition = definition, Example = example, Weight = 100.0, AppearCnt = 0)

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
        # if(cnt >= 20):
        #     break

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
