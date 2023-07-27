import requests
from django.shortcuts import render
from django import forms
import pygal  

#How to fetch from a env file (TBD HW-2)
api_key = "99033f8fe5554466ac9ef2e7657a10fc"

class NutrientForm(forms.Form):
    minCalories = forms.IntegerField(label = "Minimum calories", widget=forms.TextInput(attrs={'placeholder': 100}))
    maxCalories = forms.IntegerField(label = "Maximum calories", required=False)
    minCarbs = forms.IntegerField(min_value=0, label = "Minimum carbs(grams)", required=False)
    maxCarbs = forms.IntegerField(min_value=0, label = "Maximum carbs(grams)", required=False)
    minProtein = forms.IntegerField(min_value=0, label = "Minimum protein(grams)", required=False)
    maxProtein = forms.IntegerField(min_value=0, label = "Maximum protein(grams)", required=False)
    minFat = forms.IntegerField(min_value=0, label = "Minimum fat(grams)", required=False)
    maxFat = forms.IntegerField(min_value=0, label = "Maximum fat(grams)", required=False)
    saved_list_name = forms.CharField(max_length=127, label = "Diet Plan Name", required=False)
    
# Helper function
def spoonacular_api_call(request):
	#Spoonacular API url
	url = "https://api.spoonacular.com/recipes/findByNutrients?apiKey="+ api_key + "&number=5"

	query_str = ''
	for key, value in request.GET.items():
		if len(value) != 0:
			query_str += '&' + key + '=' + value

	#Form the complete API url 
	url+=query_str
	print(url)

	# params ={
	# 	'apiKey' : api_key,
	# 	'number' : 5,
	# 	'minCalories' : request.GET.get('minCalories'),
	# 	'maxCalories' : request.GET.get('maxCalories'),
	# 	'minCarbs' : request.GET.get('minCarbs'),
	# 	'maxCarbs' : request.GET.get('maxCarbs'),
	# 	'minProtein' : request.GET.get('minProtein'),
	# 	'maxProtein' : request.GET.get('maxProtein'),
	# 	'minFat' : request.GET.get('minFat'),
	# 	'maxFat' : request.GET.get('maxFat'),
	# }
	# print(params)
	response = requests.get(url)
	# print(response)
	return response.json()

# Create your views here.
def homepage(request):
	print('Homepage')
	
	form = NutrientForm() # Make a new blank form
	context = {
		'form': form,
	}
	return render(request, 'homepage.html', context)

def search_recipes(request):
	print('In search recipes view')
	

	if 'minCalories' in request.GET:
		form = NutrientForm(request.GET) # Make a form instance from GET data
	
		if form.is_valid(): # Check if valid (and as side-effect, generate cleaned_data dict)
			recipe_data = spoonacular_api_call(request)
			#Loop through the recipe_data list
			for recipe in recipe_data:
				recipe_id = recipe['id']
				#Set the recipe url(another api call)
				recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=false&apiKey={api_key}'
				print(recipe_url)
				recipe_info = requests.get(recipe_url).json()
				#Add another field recipe_link to the recipe json
				recipe['recipe_link'] = recipe_info['sourceUrl']

	else:
		form = NutrientForm()
		
	context = {
		'recipes' : recipe_data,
		
	}
	return render(request, 'recipes.html', context)

def compare_calories(request):
	print('In compare calories view')

	recipe_data = spoonacular_api_call(request)

	# Extracting the titles and calories from the API response
	titles = [recipe['title'] for recipe in recipe_data]
	calories = [recipe['calories'] for recipe in recipe_data]

	bar_chart = pygal.Bar()
	bar_chart.title = 'Calories per Recipe'
	#bar_chart.x_labels = titles
	
	# Adding the data to the chart 
	for idx, calorie in enumerate(calories):
		bar_chart.add(titles[idx], [calorie])

	# Displaying the color legend 
	bar_chart.legend_at_right = True
	bar_chart.x_label_rotation = 30

	chart_svg_as_datauri = bar_chart.render_data_uri()

	context = {
		"rendered_chart_svg_as_datauri": chart_svg_as_datauri,
	}

	return render(request, 'calorie_comparision.html', context)

def nutrient_breakdown(request):
	print('In nutrient breakdown view')

	recipe_data = spoonacular_api_call(request)
	titles = [recipe['title'] for recipe in recipe_data]

	#Plot a stacked bar chart having breakdown of protein, fat and carbs for each recipe
	bar_chart = pygal.StackedBar()
	bar_chart.title = 'Nutrient breakdown of recipes'
	bar_chart.x_labels = titles
	bar_chart.x_label_rotation = 30
	#Convert the protein/fat/carbs values received from API to int for plotting
	bar_chart.add('Protein', [int(recipe['protein'][:-1]) for recipe in recipe_data])
	bar_chart.add('Fat',  [int(recipe['fat'][:-1]) for recipe in recipe_data])
	bar_chart.add('Carbs', [int(recipe['carbs'][:-1]) for recipe in recipe_data])
	
	#Include chart on HTML page	
	bar_as_datauri = bar_chart.render_data_uri()

	context={
		"rendered_chart_svg_as_datauri": bar_as_datauri,
	}
	return render(request, 'calorie_comparision.html', context)