import requests
from django.shortcuts import render
import pygal  

api_key = "99033f8fe5554466ac9ef2e7657a10fc"
# Helper functions
def spoonacular_api_call(request):
	 #How to fetch from a env file (TBD HW-2)
	url = "https://api.spoonacular.com/recipes/findByNutrients?apiKey="+ api_key + "&number=10"

	query_str = ''
	min_cals = request.GET['minCalories'] if request.GET['minCalories'] else 400
	query_str += '&minCalories='+str(min_cals)

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

	for recipe in recipe_data:
		recipe_id = recipe['id']
		recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=false&apiKey={api_key}'
		print(recipe_url)
		recipe_info = requests.get(recipe_url).json()
		recipe['recipe_link'] = recipe_info['sourceUrl']
		#recipe['recipe_link'] = f'https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=false'

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

	#recipe_data = spoonacular_api_call(request)

	pie_chart = pygal.Pie()
	pie_chart.title = 'Browser usage in February 2012 (in %)'
	pie_chart.add('IE', 19.5)
	pie_chart.add('Firefox', 36.6)
	pie_chart.add('Chrome', 36.3)
	pie_chart.add('Safari', 4.5)
	pie_chart.add('Opera', 2.3)
	pie_as_datauri = pie_chart.render_data_uri()


	# # Extracting the titles and calories from the API response
	# titles = [recipe['title'] for recipe in recipe_data]
	# calories = [recipe['calories'] for recipe in recipe_data]

	# bar_chart = pygal.Bar()
	# bar_chart.title = 'Calories per Recipe'
	# #bar_chart.x_labels = titles
	
	# # Adding the data to the chart 
	# for idx, calorie in enumerate(calories):
	# 	bar_chart.add(titles[idx], [calorie])

	# # Displaying the color legend 
	# bar_chart.legend_at_right = True
	# bar_chart.x_label_rotation = 30

	# chart_svg_as_datauri = bar_chart.render_data_uri()

	context={
		"rendered_chart_svg_as_datauri": pie_as_datauri,
	}
	return render(request, 'calorie_comparision.html', context)