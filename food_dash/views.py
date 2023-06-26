from django.shortcuts import render

# Create your views here.

def homepage(request):
	print('Testing')
	context = {
	}
	return render(request, 'homepage.html', context)

