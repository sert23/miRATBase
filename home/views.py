from django.shortcuts import render
import json
from miRATBase.settings import MIRBASE_DICT
# Create your views here.


def index_view(request):

    #generate search list
    search_list = ["hsa-miR-34a-5p", "hsa-miR-7-5p"]


    return render(request, 'index.html', {'description': "z",
                                          "search_list" : json.dumps(search_list)

                                          })


def build_mirbase_link(mirna):
    # base_site = "http://www.mirbase.org/"
    mir_dict = json.load(MIRBASE_DICT)
    mima = mir_dict.get(mirna)
    if mima:
        # link = "http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc={}".format(mima)
        link = "http://mirbase.org/cgi-bin/mature.pl?mature_acc={}".format(mima)
    else:
        link = "http://www.mirbase.org/textsearch.shtml?q={}".format(mima)

    return link


def build_mirgenedb_link(mirna):
    link = "https://mirgenedb.org/browse?qtype=mbid&org=ALL&query={}".format(mirna)
    return link


def build_mircarta_link(mirna):
    link = "https://mircarta.cs.uni-saarland.de/search_box/{}".format(mirna)
    return link
