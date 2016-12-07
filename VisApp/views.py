from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import numpy as np

import json
import csv
import os


# Create your views here.
def main(request):
	return render(request, 'main.html')

def data(request):
	return render(request, 'data.html')

def uploadFile(request):
	os.remove(settings.MEDIA_ROOT + "/data.csv")
	csv = request.FILES['file']
	fs = FileSystemStorage()
	filename = fs.save("data.csv", csv)

	return redirect('../data')

def overview(request):
	return render(request, 'overview.html')

def preprocess_csv(selected_column_names=["x","y"]):
	with open(settings.STATIC_ROOT + "/test.csv","r") as f:
		data = list(csv.DictReader(f))
		selected_data = []
		for row in data:
			selected_row = dict([(key,row[key]) for key in selected_column_names])
			selected_data.append(selected_row)

		return selected_data

def convert4train(data):
    return [row.values() for row in data]

def do_kmeans(K=2, max_iter=300, n_init=10):
	data = preprocess_csv()

	kmeans = KMeans(n_clusters=K,max_iter=max_iter,n_init=n_init).fit(convert4train(data))
	for i, row in enumerate(data):
	    data[i]["class"] = str(kmeans.labels_[i])
	
	return data

def do_dbscan(eps=0.5, min_samples=5):
	data = preprocess_csv()

	dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(convert4train(data))
	for i, row in enumerae(data):
		data[i]["class"] = str(dbscan.labels_[i])

	return data

def kmeans(request):
	selected_column_names = ["x","y"]

	result = do_kmeans()
	return render(request, 'kmeans.html', {"data": tuple(result)})

def ajax_kmeans(request):
	K = int(request.GET["K"].encode("utf-8"))
	max_iter = int(request.GET["max_iter"].encode("utf-8"))
	n_init = int(request.GET["n_init"].encode("utf-8"))
	selected_column_names = ["x","y"]

	result = do_kmeans(K, max_iter, n_init)
	mimetype = "application/json"
	return HttpResponse(json.dumps(result), mimetype)

def dbscan(request):
	selected_column_names = ["x","y"]

	result = do_dbscan()
	return render(request, 'dbscan.html', {"data": tuple(result)})

def ajax_dbscan(request):
	eps = int(request.GET["eps"].encode("utf-8"))
	min_samples = int(request.GET["min_samples"].encode("utf-8"))
	selected_column_names = ["x","y"]

	result = do_dbscan(eps=eps, min_samples=min_samples)
	mimetype = "application/json"
	return HttpResponse(json.dumps(result), mimetype)

def hierarchical(request):
	return render(request, 'hierarchical.html')













