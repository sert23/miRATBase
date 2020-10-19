from django.shortcuts import render
import json
from miRATBase.settings import MIRBASE_DICT, MEDIA_ROOT, MEDIA_URL
from home.models import MiRNA, Gene, Pathway, TargetGene, PathwayGene
from django.http import JsonResponse
import os

import pandas as pd
# Create your views here.


def index_view(request):

    #generate search list
    mirna_list = list(TargetGene.objects.all().values_list('mirna', flat=True))
    gene_list = list(TargetGene.objects.all().values_list('gene', flat=True))

    pathway_list = list(PathwayGene.objects.all().values_list('pathway', flat=True))

    search_list = list(set(mirna_list)) + list(set(gene_list)) + list(set(pathway_list))

    return render(request, 'index.html', {'description': "z",
                                          "search_list": json.dumps(search_list)

                                          })

def build_mirbase_link(mirna):
    # base_site = "http://www.mirbase.org/"
    with open(MIRBASE_DICT,"r") as mdf:
        mir_dict = json.load(mdf)
    mima = mir_dict.get(mirna)
    if mima:
        # link = "http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc={}".format(mima)
        link = "http://mirbase.org/cgi-bin/mature.pl?mature_acc={}".format(mima)
    else:
        link = "http://www.mirbase.org/textsearch.shtml?q={}".format(mima)

    return link


def build_mirgenedb_link(mirna):
    query = MiRNA.objects.filter(name=mirna).values_list('mirgenedb', flat=True)
    name = list(query)[0]
    print(name)
    link = "https://mirgenedb.org/show/hsa/{}".format(name).replace("Hsa-","")
    return link


def build_mircarta_link(mirna):
    link = "https://mircarta.cs.uni-saarland.de/search_box/{}".format(mirna)
    return link

def build_NCBI_link(gene):
    link = "https://www.ncbi.nlm.nih.gov/gene/?term={}".format(gene)
    return link


def build_mirtarbase(gene,mirna):

    link1 = "http://mirtarbase.cuhk.edu.cn/php/search.php?org=hsa&opt=mirna_id&kw={}".format(mirna)
    link2 = "http://mirtarbase.cuhk.edu.cn/php/search.php?org=hsa&kw={}&opt=target".format(gene)
    # both
    link3 = "http://mirtarbase.cuhk.edu.cn/php/search.php?org=hsa&mirnas={}&targets={}&opt=adv".format(mirna,gene)

    return link1,link2,link3

def yesOrNo(input_bool):
    if input_bool:
        return "Yes"
    else:
        return "No"

def search_view(request):

    context = {}

    search_string = request.GET.get("search_term")
    # search_string = "VAMP2"
    # search_string = "hsa-miR-34a-5p"

    mirna_list = list(TargetGene.objects.all().values_list('mirna', flat=True))
    gene_list = list(TargetGene.objects.all().values_list('gene', flat=True))
    pathway_list = list(PathwayGene.objects.all().values_list('pathway', flat=True))

    found = True

    if search_string in mirna_list:
        query = TargetGene.objects.filter(mirna=search_string)
        val_table = list(query.values_list("mirna","gene","status","rlu"))

    elif search_string in gene_list:

         query = TargetGene.objects.filter(gene=search_string)
         val_table = list(query.values_list("mirna", "gene", "status","rlu"))
    elif search_string in pathway_list:

        query = PathwayGene.objects.filter(pathway=search_string)
        genes = list(query.values_list("gene", flat=True))
        query2 = TargetGene.objects.filter(gene__in=genes)
        val_table = list(query2.values_list("mirna", "gene", "status", "rlu"))

    else:
        found = False

    # query = TargetGene.objects.all()
    # val_table = list(query.values_list("mirna","gene","status"))

    js_headers = json.dumps([{"title": "miRNA"},
                             {"title": "Gene"},
                             {"title": "RLU"},
                             # { "title": "Select" }])
                             {"title": 'Validated'},
                             {"title": 'Search miRTarBase'}
                             ])
    js_body = []
    if found:
        for row in val_table:
            mirna = '<a onclick="popMir(\'' + row[0] + '\');" href="javascript:void(0)" >' + row[0] + '</a>'
            gene = '<a href="' + build_NCBI_link(row[1]) + '">' + row[1] + '</a>'
            mirtarbase = '<a onclick="popMirTar(\'' + "','".join([row[0],row[1]]) + '\');" href="javascript:void(0)" > Click to search</a>'

            js_body.append([mirna,gene, row[3], yesOrNo(bool(row[2])) , mirtarbase])
        href = "javascript:void(0)"
        context["headers"] = js_headers
        context["tbody"] = json.dumps(js_body)
    context["search_term"] = search_string
    context["found"] = found

    return render(request, 'search.html', context)


def download_view(request):

    context = {}

    data_folder = os.path.join(MEDIA_ROOT, "HiTmiR_tables")

    mir_files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder,f))]

    links = [ [os.path.join(data_folder,f).replace(MEDIA_ROOT,MEDIA_URL),f.replace("HiTmiR_results_","").replace(".tsv","")]
              for f in mir_files ]

    context["links"] = links

    return render(request, 'downloads.html', context)

def about_view(request):

    context = {}

    return render(request, 'about.html', context)


def ajax_mirna(request):
    mirna = request.GET.get("mirna")

    data = {}
    data["mirbase"] = build_mirbase_link(mirna)
    data["mirgenedb"] = build_mirgenedb_link(mirna)
    data["mircarta"] = build_mircarta_link(mirna)

    return JsonResponse(data)

def ajax_mirtarbase(request):
    mirna = request.GET.get("mirna")
    gene = request.GET.get("gene")

    link1,link2,link3 = build_mirtarbase(gene, mirna)

    data = {}
    data["mirna"] = link1
    data["gene"] = link2
    data["both"] = link3

    return JsonResponse(data)


def view_all(request):

    term = request.GET.get("term")


    if term == "mirnas":
        entry_list = list(TargetGene.objects.all().values_list('mirna', flat=True))
        entry_string = "miRNAs"
    elif term == "genes":
        entry_list = list(TargetGene.objects.all().values_list('gene', flat=True))
        entry_string = "genes"
    elif term == "paths":
        entry_list = list(PathwayGene.objects.all().values_list('pathway', flat=True))
        entry_string = "pathways"

    context = {}
    context["entry_list"] = set(entry_list)
    context["term"] = entry_string

    return render(request, 'all.html', context)
