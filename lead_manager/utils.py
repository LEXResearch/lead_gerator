import requests as r
import random
from bs4 import BeautifulSoup

from .models import LeadModel, LeadGerated, Subject

URL = "http://repositorio.ufsm.br/handle/1/{}?show=full"

def get_docs():
    for doc in range(10):
        data = r.get(URL.format((doc+10000)))
        if data:
            soup = BeautifulSoup(data.text, 'html.parser')

            lc, subjects = get_content(soup) #lc short for lead_content

            id_from_manancial = doc+10000
            # get a model to use
            lead_model = get_random_lead_model()
            lead = lead_model.description

            ob_subjects = []

            for sub in subjects:
                try:
                    s = Subject.objects.get(name=sub)
                    ob_subjects.append(s)
                except Subject.DoesNotExist:
                    ob_subjects.append(Subject.objects.create(name=sub))

            lead = lead.format(title=lc['title'], type=lc['type'],
                author=lc['author'], advisor=lc['advisor'],
                subjects=lc['subjects'], program=lc['program'], link=lc['link'])

            ltype = lc['type'][0].lower()

            lead_created = LeadGerated.objects.create(title=lc['title'],
                description=lead, author=lc['author'], advisor=lc['advisor'],
                id_from_manancial=id_from_manancial, program=lc['program'],
                type=type, lead_model=lead_model)

            for sub in ob_subjects:
                lead_created.subjects.add(sub)

def get_content(soup):
    subjects = soup.find_all("meta", attrs={'name':"DC.subject", 'xml:lang':'por'})
    subjects = [subj['content'] for subj in subjects if len(subj['content']) < 30]

    subject_content = ''
    for i, sub in enumerate(subjects):
        if i < 1:
            subject_content += sub.lower() + ", "
        elif i == 2:
            subject_content += sub.lower() + " e "
        elif i == 3:
            subject_content += sub.lower()

    program = soup.find_all("meta", attrs={'name':'DC.publisher'})
    program = [pro for pro in program if "programa" in pro['content'].lower()]

    author = soup.find_all("meta", attrs={'name':'DC.creator'})[0]['content'].split(", ")
    author = author[1] + " " + author[0]

    advisor = soup.find_all("meta", attrs={'name':'DC.contributor'})[0]['content'].split(", ")
    advisor = advisor[1] + " " + advisor[0]

    lead_content = {
        'title': soup.find_all("meta", attrs={'name':'DC.title'})[0]['content'],
        'author': author,
        'type': soup.find_all("meta", attrs={'name':'DC.type'})[0]['content'],
        'program': program[0]['content'],
        'advisor': advisor,
        'subjects': subject_content,
        'link': "<a href='www.google.com'>Repositório Manacial</a>",
    }
    return lead_content, subjects

def get_random_lead_model():
    models = LeadModel.objects.all()
    if models:
        return random.choice(models)
    else:
        return []
