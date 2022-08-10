from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.views.generic.base import TemplateView


from google_maps_apis_project.mixins import Directions

class HomeView(TemplateView):
	'''
	Generic FormView with our mixin to display user home page
	'''
	template_name = "main/home.html"

def route(request):
	'''
	Basic view for routing
	'''
	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"base_country": settings.BASE_COUNTRY}
	return render(request, 'main/route.html', context)

def map(request):
	'''
	Basic view for displaying a map
	'''
	lat_a = request.GET.get("lat_a", None)
	long_a = request.GET.get("long_a", None)
	lat_b = request.GET.get("lat_b", None)
	long_b = request.GET.get("long_b", None)
	address_a = request.GET.get("address_a", None)
	address_b = request.GET.get("address_b", None)

	# pass all variables to API call
	if lat_a and lat_b and long_a and long_b and address_a and address_b:
		directions = Directions(
			lat_a= lat_a,
			long_a=long_a,
			lat_b = lat_b,
			long_b=long_b,
			address_a=address_a,
			address_b=address_b,
			)
	else:
		return redirect(reverse('main:route'))

	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"base_country": settings.BASE_COUNTRY,
	"lat_a": lat_a,
	"long_a": long_a,
	"lat_b": lat_b,
	"long_b": long_b,
	"origin": f'{lat_a}, {long_a}',
	"destination": f'{lat_b}, {long_b}',
	"directions": directions,

	}
	return render(request, 'main/map.html', context)
