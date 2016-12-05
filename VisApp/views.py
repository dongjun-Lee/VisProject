from django.shortcuts import render

# Create your views here.
def main(request):
	return render(request, 'main.html')

def data(request):
	return render(request, 'data.html')

def overview(request):
	return render(request, 'overview.html')