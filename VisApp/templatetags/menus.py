from django import template

register = template.Library()

@register.assignment_tag
def get_menu_list():
	menus =	[
		{'title' : 'Data', 'url' : '/data/'},
		{'title' : 'Overview', 'url' : '/overview/'},
		{'title' : 'K-means', 'url' : '/kmeans/'},
		{'title' : 'DBSCAN', 'url' : '/dbscan/'},
	]
	return menus