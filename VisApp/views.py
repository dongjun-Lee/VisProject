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

def load_csv():
	with open(settings.MEDIA_ROOT + "/data.csv","r") as f:
		data = list(csv.DictReader(f))
		return data

def project_data(data, columns):
	selected_data = []
	for row in data:
		selected_row = dict([(key,row[key]) for key in columns])
		selected_data.append(selected_row)

	return selected_data

def conv2array(data):
	return np.array([row.values() for row in data])

def do_clustering(vis_columns=[],cal_columns=[],method="kmeans",K=2,max_iter=300,eps=1.5,min_samples=5):
	data = load_csv()
	columns = sorted(list(data[0].keys()))
	if not vis_columns:
		vis_columns = columns[:2]
	if not cal_columns:
		cal_columns = columns

	training_data = project_data(data,cal_columns)

	if method == "kmeans":
		result = KMeans(n_clusters=K, max_iter=max_iter).fit(conv2array(training_data))
	else:
		result = DBSCAN(eps=eps, min_samples=min_samples).fit(conv2array(training_data))
		
	for i, row in enumerate(data):
		data[i]["class_label"] = str(result.labels_[i])

	vis_column_dics = [dict([("name", c), ("selected", c in vis_columns)]) for c in columns]
	cal_column_dics = [dict([("name", c), ("selected", c in cal_columns)]) for c in columns]
	return data, project_data(data, vis_columns+["class_label"]), vis_column_dics, cal_column_dics

def save_csv(result):
	with open(settings.MEDIA_ROOT + "/result.csv", "w") as f:
		w = csv.DictWriter(f, fieldnames=result[0].keys(), delimiter=",")
		w.writeheader()
		for row in result:
			w.writerow(row)

def kmeans(request):
	result, selected_result, vis_columns, cal_columns = do_clustering(method="kmeans")
	save_csv(result)

	return render(request, 'kmeans.html', {
		"data": tuple(selected_result),
		"vis_columns": tuple(vis_columns),
		"cal_columns": tuple(cal_columns)
	})

def dbscan(request):
	result, columns = do_clustering(method="dbscan")
	return render(request, 'dbscan.html', {"data": tuple(result)})

def ajax_kmeans(request):
	K = int(request.GET["K"].encode("utf-8"))
	max_iter = int(request.GET["max_iter"].encode("utf-8"))
	selected_vis_columns = [element.encode("utf-8") for element in request.GET.getlist("vis_columns[]")]
	selected_cal_columns = [element.encode("utf-8") for element in request.GET.getlist("cal_columns[]")]

	result, selected_result, _, _ = do_clustering(vis_columns=selected_vis_columns, cal_columns=selected_cal_columns, method="kmeans", K=K, max_iter=max_iter)
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













