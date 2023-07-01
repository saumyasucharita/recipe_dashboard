import requests
from django.shortcuts import render
import pygal  

#How to fetch from a env file (TBD HW-2)
api_key = "99033f8fe5554466ac9ef2e7657a10fc"
# Helper function
def spoonacular_api_call(request):
	#Spoonacular API url
	url = "https://api.spoonacular.com/recipes/findByNutrients?apiKey="+ api_key + "&number=10"

	query_str = ''
	#Set minCalories to 400 if the user has not provided the value in form
	min_cals = request.GET['minCalories'] if request.GET['minCalories'] else 400
	query_str += '&minCalories='+str(min_cals)

	#Check if we have received the query parameters
	if 'maxCalories' in request.GET:
		if len(request.GET['maxCalories']) != 0:
			query_str += '&maxCalories='+request.GET['maxCalories']

	if 'minCarbs' in request.GET:
		if len(request.GET['minCarbs']) != 0:
			query_str += '&minCarbs='+request.GET['minCarbs']

	if 'maxCarbs' in request.GET:
		if len(request.GET['maxCarbs']) != 0:
			query_str += '&maxCarbs='+request.GET['maxCarbs']

	if 'minProtein' in request.GET:
		if len(request.GET['minProtein']) != 0:
			query_str += '&minProtein='+request.GET['minProtein']
	
	if 'maxProtein' in request.GET:
		if len(request.GET['maxProtein']) != 0:
			query_str += '&maxProtein='+request.GET['maxProtein']

	if 'minFat' in request.GET:
		if len(request.GET['minFat']) != 0:
			query_str += '&minFat='+request.GET['minFat']

	if 'maxFat' in request.GET:
		if len(request.GET['maxFat']) != 0:
			query_str += '&maxFat='+request.GET['maxFat']

	#Form the complete API url 
	url+=query_str
	print(url)

	response = requests.get(url)
	return response.json()

# Create your views here.
def homepage(request):
	print('Homepage')
	context = {
	}
	return render(request, 'homepage.html', context)

def search_recipes(request):
	print('In search recipes view')
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