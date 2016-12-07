from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

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

def do_kmeans(K,max_iter,n_init,selected_column_names):
	with open(settings.STATIC_ROOT + "/test.csv","r") as f:
		data = list(csv.DictReader(f))

		selected_dics = []
		selected_list = []
		for row in data:
			selected_row = dict([(key,row[key]) for key in selected_column_names])
			selected_dics.append(selected_row)
			selected_list.append(selected_row.values())

	kmeans = KMeans(n_clusters=K,max_iter=max_iter,n_init=n_init).fit(selected_list)

	for i, row in enumerate(selected_dics):
		selected_dics[i]["class"] = str(kmeans.labels_[i])
	
	return selected_dics

def kmeans(request):
	K = 2
	max_iter = 300
	n_init = 10
	selected_column_names = ["x","y"]

	result = do_kmeans(K,max_iter,n_init,selected_column_names)
	return render(request, 'kmeans.html', {"data": tuple(result)})

def ajax_kmeans(request):
	K = int(request.GET["K"].encode('utf-8'))
	max_iter = int(request.GET["max_iter"].encode('utf-8'))
	n_init = int(request.GET["n_init"].encode('utf-8'))
	selected_column_names = ["x","y"]

	result = do_kmeans(K, max_iter, n_init,selected_column_names)
	mimetype = "application/json"
	return HttpResponse(json.dumps(result), mimetype)

def dbscan(request):
	return render(request, 'dbscan.html')


