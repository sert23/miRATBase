from django.db import models
import re

class MiRNA(models.Model):
    name = models.CharField(max_length=100)
    mirgenedb = models.CharField(max_length=100, default=" ")

    def load_new(input_mir, input_mirdb):
        genes = MiRNA.objects.all().values_list('name', flat=True)
        if not (input_mir in genes):
            MiRNA.objects.create(
                name=input_mir,
                mirgenedb=input_mirdb)


class Gene(models.Model):
    name = models.CharField(max_length=100)

    @staticmethod
    def load_new(input_gene):
        genes = Gene.objects.all().values_list('name', flat=True)
        if not (input_gene in genes):
            Gene.objects.create(
                name=input_gene)

    @staticmethod
    def load_from_file(input_file):

        with open(input_file, "r") as mf:
            lines = mf.readlines()

        for line in lines[1:]:
            row = line.split("\t")
            gene_name = row[1].rstrip()
            Gene.load_new(gene_name)

    @staticmethod
    def delete_entries():
        Gene.objects.all().delete()

class Pathway(models.Model):
    name = models.CharField(max_length=200)

    @staticmethod
    def load_new(input_gene):
        Pathway.objects.create(
            name=input_gene)

    @staticmethod
    def load_from_file(input_file):

        with open(input_file, "r") as mf:
            lines = mf.readlines()

        for line in lines[1:]:
            row = line.split("\t")
            path_name = row[1].rstrip()
            pathways = Pathway.objects.all().values_list('name', flat=True)

            if not (path_name in pathways):
                print(path_name)
                Pathway.load_new(path_name)

class TargetGene(models.Model):
    mirna = models.CharField(max_length=100)
    gene = models.CharField(max_length=100)
    both = models.CharField(max_length=100, default=";")
    rlu = models.FloatField(default=0)
    status = models.BooleanField()


    @staticmethod
    def load_from_file(input_file,input_mirna):
        with open(input_file, "r") as mf:
            lines = mf.readlines()

        target_dict = {}
        rlu_dict = {}


        for line in lines[1:]:
            row = line.rstrip().split("\t")
            pair = (input_mirna,row[1])
            print(pair)
            if not target_dict.get(pair):
                target_dict[pair] = bool(int(row[-1]))
            old_rlu = rlu_dict.get(pair)
            new_rlu = float(row[-3])
            if old_rlu:
                if new_rlu < old_rlu:
                    rlu_dict[pair] = new_rlu
            else:
                rlu_dict[pair] = new_rlu


        for k in target_dict.keys():
            targets = TargetGene.objects.all().values_list('both', flat=True)
            pair = k[0] + ";" + k[1]
            if not pair in targets:
                TargetGene.objects.create(
                    mirna=k[0],
                    gene=k[1],
                    both=pair,
                    status=target_dict.get(k),
                    rlu=rlu_dict.get(k),
                    )

class PathwayGene(models.Model):
    pathway = models.CharField(max_length=200)
    gene = models.CharField(max_length=100)
    db = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100)


    @staticmethod
    def load_from_file(input_file):
        with open(input_file, "r") as mf:
            lines = mf.readlines()

        for line in lines[2:]:
            row = line.split("\t")

            database = row[0]
            name = row[1]
            ident = row[2]
            targets = row[4]

            for t in targets.split(","):
                PathwayGene.objects.create(
                    pathway=name,
                    gene=t,
                    db=database,
                    identifier=ident)

    @staticmethod
    def purge_names():
        have_brackets = PathwayGene.objects.filter(pathway__regex=r".*\(.*\)")

        for p in have_brackets:

            current = p.pathway
            new = re.sub(r'(\([0-9]\))', '', current)
            p.pathway = new
            p.save()
        have_ampersand = PathwayGene.objects.filter(pathway__regex=r".*&")
        for p in have_ampersand:
            current = p.pathway
            new = current.replace("&", " and ")
            p.pathway = new
            p.save()

class Validations(models.Model):
    mirna = models.CharField(max_length=100)
    pathway = models.CharField(max_length=200)
    gene = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    @staticmethod
    def load_from_file(input_file):
        with open(input_file, "r") as mf:
            lines = mf.readlines()

        for line in lines[1:]:
            row = line.split("\t")



