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

	with open(settings.STATIC_ROOT + "/test.csv","r") as f:
		data = list(csv.reader(f, delimiter=','))
		column_names = data[0]
		data = [[float(i) for i in row][:-1] for row in data[1:]]

	kmeans = KMeans(n_clusters=6).fit(data)

	for i, row in enumerate(data):
		row.append(kmeans.labels_[i])
	print(data)

	return render(request, 'kmeans.html')

def dbscan(request):
	return render(request, 'dbscan.html')


