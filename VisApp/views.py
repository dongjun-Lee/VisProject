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

def load_csv(selected_columns):
	with open(settings.STATIC_ROOT + "/test.csv","r") as f:
		data = list(csv.DictReader(f))
		selected_data = []
		for row in data:
			selected_row = dict([(key,row[key]) for key in selected_columns])
			selected_data.append(selected_row)

		return selected_data

def conv2array(data):
    return np.array([row.values() for row in data])

def do_kmeans(selected_columns, K=2, max_iter=300, n_init=10):
	data = load_csv(selected_columns)
	columns = data[0].keys()

	kmeans = KMeans(n_clusters=K, max_iter=max_iter, n_init=n_init).fit(conv2array(data))
	for i, row in enumerate(data):
	    data[i]["class"] = str(kmeans.labels_[i])
	
	return data, columns

def do_dbscan(selected_columns, eps=1.5, min_samples=5):
	data = load_csv(selected_columns)

	dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(conv2array(data))
	for i, row in enumerate(data):
		data[i]["class"] = str(dbscan.labels_[i])

	return data

def make_column_dics(columns, selected_columns):
	 return [dict[("name", c), ("selected", c in selected_columns)] for c in columns]
			result.append(dict[("name",c), ("selected",False)])
	return [dict[("name", c), ("selected", (c in selected_columns))] for c in columns]

def kmeans(request):
	selected_columns= ["x","y"]
	result, columns = do_kmeans(selected_columns)
		tuple(make_column_dics(columns, seleted_columns))})
	return render(request, 'kmeans.html', {"data": tuple(result), "columns":
		tuple(make_column_dics(columns, selected_columns))})

def ajax_kmeans(request):
	K = int(request.GET["K"].encode("utf-8"))
	max_iter = int(request.GET["max_iter"].encode("utf-8"))
	n_init = int(request.GET["n_init"].encode("utf-8"))
	selected_columns= ["x","y"]

	result = do_kmeans(selected_columns, K, max_iter, n_init)
	mimetype = "application/json"
	return HttpResponse(json.dumps(result), mimetype)

def dbscan(request):
	selected_columns= ["x","y"]

	result = do_dbscan(selected_columns)
	return render(request, 'dbscan.html', {"data": tuple(result)})

def ajax_dbscan(request):
	eps = float(request.GET["eps"].encode("utf-8"))
	min_samples = int(request.GET["min_samples"].encode("utf-8"))
	selected_columns= ["x","y"]

	result = do_dbscan(selected_columns, eps=eps, min_samples=min_samples)
	mimetype = "application/json"
	return HttpResponse(json.dumps(result), mimetype)

def hierarchical(request):
	return render(request, 'hierarchical.html')













