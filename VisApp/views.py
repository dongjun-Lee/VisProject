from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from sklearn.cluster import KMeans
import numpy as np

import json
import csv


# Create your views here.
def main(request):
	return render(request, 'main.html')

def data(request):
	return render(request, 'data.html')

def uploadFile(request):
	# TODO : delete original file if exists

	csv = request.FILES['file']
	fs = FileSystemStorage()
	filename = fs.save("data.csv", csv)

	return redirect('../data')

def overview(request):
	return render(request, 'overview.html')

def kmeans(request):
	N = 7
	selected_column_names = ["x","y"]

	with open(settings.STATIC_ROOT + "/test.csv","r") as f:
		data = list(csv.DictReader(f))

		selected_dics = []
		selected_list = []
		for row in data:
			selected_row = dict([(key,row[key]) for key in selected_column_names])
			selected_dics.append(selected_row)
			selected_list.append(selected_row.values())

	kmeans = KMeans(n_clusters=N).fit(selected_list)

	for i, row in enumerate(selected_dics):
		selected_dics[i]["class"] = str(kmeans.labels_[i])

	return render(request, 'kmeans.html', {"data": tuple(selected_dics)})

def dbscan(request):
	return render(request, 'dbscan.html')


