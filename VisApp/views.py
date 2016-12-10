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
	with open(settings.MEDIA_ROOT + "/data.csv","r") as f:
		data = list(csv.DictReader(f))
		if not selected_columns:
			selected_columns = sorted(list(data[0].keys()))[0:2]
		selected_data = []
		for row in data:
			selected_row = dict([(key,row[key]) for key in selected_columns])
			selected_data.append(selected_row)

		return data, selected_data, selected_columns

def conv2array(data):
	return np.array([row.values() for row in data])

def do_clustering(selected_columns=[],method="kmeans",K=2,max_iter=300,eps=1.5,min_samples=5):
	data, selected_data, selected_columns = load_csv(selected_columns)
	columns = sorted(list(data[0].keys()))

	if method == "kmeans":
		result = KMeans(n_clusters=K, max_iter=max_iter).fit(conv2array(data))
	else:
		result = DBSCAN(eps=eps, min_samples=min_samples).fit(conv2array(data))
		
	for i, row in enumerate(data):
		data[i]["class"] = str(result.labels_[i])
		selected_data[i]["class"] = str(result.labels_[i])

	column_dics = [dict([("name", c), ("selected", c in selected_columns)]) for c in columns]

	return data, selected_data, column_dics

def save_csv(result):
	with open(settings.MEDIA_ROOT + "/result.csv", "w") as f:
		w = csv.DictWriter(f, fieldnames=result[0].keys(), delimiter=",")
		w.writeheader()
		for row in result:
			w.writerow(row)

def kmeans(request):
	result, selected_result, columns = do_clustering(method="kmeans")
	save_csv(result)
	return render(request, 'kmeans.html', {"data": tuple(selected_result), "columns": tuple(columns)})

def dbscan(request):
	result, columns = do_clustering(method="dbscan")
	return render(request, 'dbscan.html', {"data": tuple(result)})

def ajax_kmeans(request):
	K = int(request.GET["K"].encode("utf-8"))
	max_iter = int(request.GET["max_iter"].encode("utf-8"))
	selected_columns = [element.encode("utf-8") for element in request.GET.getlist("columns[]")]

	result, selected_result, columns = do_clustering(selected_columns=selected_columns, method="kmeans", K=K, max_iter=max_iter)
	save_csv(result)
	mimetype = "application/json"
	return HttpResponse(json.dumps(selected_result), mimetype)

def ajax_dbscan(request):
	eps = float(request.GET["eps"].encode("utf-8"))
	min_samples = int(request.GET["min_samples"].encode("utf-8"))
	selected_columns = [element.encode("utf-8") for element in request.GET.getlist("columns[]")]

	result, columns = do_clustering(seleted_columns=selected_columns, method="dbscan", eps=eps, min_samples=min_samples)
	mimetype = "application/json"
	return HttpResponse(json.dumps(result), mimetype)

def hierarchical(request):
	return render(request, 'hierarchical.html')













