# NutriCO2

Completed during my 9th week on General Assembly\'s Software Engineering Immersive, NutriCO2 is a recipe app that calculates CO2 emissions and nutritional data for a given recipe. This project was built using PostgreSQL, Python, Django, Bootstrap, HTML and CSS.

**NutriCO2 is deployed at https://nutrico2.skreslett.com**

You can try out NutriCO2 via the link above. NutriCO2 does not require the installation of any additional software. You can visit the website and try the recipe calculations by signing in using the following credentials:
- Username: test@skreslett.com
- Password: Pa$$word123

This project was completed as a pair within a week. My teammate for this project was Dan Emsley and his repository for this project can be found [here](http://https://github.com/Emsley1d/Project03-NutriCO2 "here").

---
| Table of Contents |
|-|
| [Technologies Used](#Technologies-Used) |
| [Brief](#Brief) |
| [Planning](#Planning) |
| [Build Process](#Build-Process) |
| [Challenges](#Challenges) |
| [Wins](#Wins) |
| [Key Learnings](#Key-Learnings) |
| [Bugs](#Bugs) |
| [Future Improvements](#Future-Improvements) |

---
## Technologies Used

- PostgreSQL
- Django
- Python
- Bootstrap
- HTML
- CSS

---
## Brief

Our brief was to create a web application of our choice from scratch in 7 days with the following requirements specified:

- Create the application using at least 2 related models, one of which should be a user
- Include all major CRUD functions for at least one of your models.
- Add authentication AND authorization (page protection) to restrict access to appropriate users.
	- User must be able to sign up or login.
	- Signed in user must be able to change password and logout.
	- change password and logout must only be available to logged in users.
- Give feedback to the user after each action, and after form. submissions with success/failure.
- Clear forms after submission failure.
- Manage team contributions and collaboration using a standard Git flow on Github.
- Layout and style your front-end with clean & well-formatted CSS, with or without a framework. Put effort into your design!
- Deploy your application online so it's publicly accessible.

---
## Planning

We spent some time discussing possible ideas that would be both interesting and practical. Dan has an interest in working in the environmental sector and I have a love for food and drink so we settled on the idea of creating a recipe app that calculates CO2 emissions and nutritional data for a given recipe. We agreed to remain on Zoom throughout and to use pair-programming in order to assist each other as needed. We distributed tasks by reflecting on the skills we wanted to develop from previous projects. We came up with the name collaboratively and once we settled on the brief we started our planning by working on Wireframes (Dan) and an ERD using Miro (myself) before working together to create a Kanban board using Trello.

# INSERT PLANNING



---
## Build Process

### Stage 1
To start off with, Dan created the folder and file structure to set up the project environment and I started collating data on CO2e emissions for food products from various publicly available sources online such as academic journals and the Research Institute of Sweden.

### Stage 2
Dan moved on to building the core page structure which involved some pair-programming via Zoom with myself. However, I would say that 60% of my time at this point was still focussed on gathering data. I ended up with more than 500 lines of data that I needed to rationalise. Using Excel I systematically sorted through and assessed the suitability of each data point, deciding whether to eliminate it or create an average value for the given ingredient if there were multiple data points. At the same time I was formatting the data for upload to PostgreSQL.

### Stage 3
I started working on implementing an Optical Character Recognition image to text API that Dan found during some early research as well as drafting the nutrition API request while Dan started working on the authorisation functionality.

### Stage 4
Whilst Dan continued working on authorisation I moved on to implementing the CRUD functionality for our ingredients and recipe data as well as implementing the emissions calculation.

Below you will find some code snippets from the stages described above.




### Highlights
#### Ocular Character Recognition
```
def method_image_to_text(request, recipe_id):
    recipe = Recipe.objects.get(id = recipe_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageTextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print('valid')

            request.encoding = 'utf-8'
            imageFile = request.FILES["image"]
            receipt_image = imageFile.read()
            
            url = "https://api.apilayer.com/image_to_text/upload"

            payload = smart_bytes(receipt_image, encoding="utf-8", strings_only=False, errors="strict")
            headers= {
            # "apikey": os.getenv('APIKEY')
            "apikey": 'j5bBeYtVScafh6Q3BmKwgobGfvawvsBZ'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            status_code = response.status_code
            result = response.text
            print(result)

            # # # # MANIPULATE RESPONSE HERE
            # # # # DO CODE!!!!
            resultJSON = json.dumps(result)
            # print(resultJSON)
            return render(request, 'main_app/image_to_text.html', {'form': form, 'result': result, 'recipe': recipe})
            # return redirect('/')
        else:
            print('not valid')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImageTextForm()
    return render(request, 'main_app/image_to_text.html', {'form': form, 'recipe': recipe})
```
This is the Ocular Character Recognition API request, the purpose of this function is to allow the user to upload an image containing words that will then be converted into editable text. This is done by first checking whether the request method is POST before building the request. We then make sure the encoding is uft-8 before building the request from the uploaded image file and the API key. Once we have the response we then render the page with the data from the response. If the request method was not POST then we render the same page without the data.

#### Calculate Carbon Emissions
```
def carbon_calculation(request, recipe_id):
    qty = IngredientQuantity.objects.filter(recipe_id = recipe_id)
    count = 0
    for q in qty:
        if q.quantity is not None and q.ingredient is not None:
            co2 = Ingredient.objects.get(id = q.ingredient.id).co2e_med
            count += (co2 * q.quantity)
            print(count)
        elif q.quantity is not None and q.custom_ingredient is not None:
            co2 = CustomIngredient.objects.get(id = q.custom_ingredient.id).co2e
            count += (co2 * q.quantity)
            print(count)
    recipe = Recipe.objects.get(id = recipe_id)
    recipe.carbon_calculation = count
    recipe.save()
    return redirect('recipe_detail', recipe_id = recipe_id)
```
This is the function I wrote for calculating the carbon emissions for a given recipe. It starts by retrieving the ingredient quantities for the given recipe, then loops through the ingredients and checks what type of ingredient it is. We have two types of ingredients, the first are pre-populated by us with verified CO2e data from our research and the second type are user created ingredients which are missing from our CO2e database. The user has the option to include the emissions data for any ingredients they add, should they have this information available. Once we know what type of ingredient we are looking at we then look up its CO2 data and multiply it by the recipe quantity before adding it to our calculation. Once the loop has completed we then save the calculation to the recipe in our database.

#### Manage Recipe, Ingredient and Quantity realtionships
```
def assoc_ingredient(request, recipe_id):
    Recipe.objects.get(id = recipe_id).ingredients.add(request.POST['ingredient'])
    row = IngredientQuantity.objects.get(recipe_id = recipe_id, ingredient_id = request.POST['ingredient'])
    row.quantity = request.POST['quantity']
    row.save()
    return redirect('recipe_detail', recipe_id = recipe_id)

def unassoc_ingredient(request, recipe_id):
    Recipe.objects.get(id = recipe_id).ingredients.remove(request.POST['ingredient'])
    return redirect('recipe_detail', recipe_id = recipe_id)
```
As our database has a many to many relationship between Ingredients, Custom Ingredients and Recipes we used an Ingredient Quantity table to bridge those relationships. This table also contains the quantity data for the recipes, so we had to use a through model. The functions above are required in order to add or remove an ingredient and its respective quantity from the Ingredient Quantity Table and as such remove the ingredient’s relationship to the given recipe. In our code there are almost identical functions for Custom Ingredients. I had wanted to merge them and the relative forms on the front-end but I wasn’t able to find a solution in the timeframe we had.

---
## Challenges
My biggest challenge was working with the many to many relationships and the through model. It permitted us to store additional data but was much more complex and consequently time consuming than I expected.

We were not able to fully overcome the challenges we encountered and consequently the project remains incomplete. Furthermore, with the benefit of hindsight it is obvious that I shouldn’t have spent such a large amount of time collecting data, whilst it is vital a project such as this is based on valid and reliable findings, I underestimated how challenging I would find it to build the site’s core functionality.

Going forward, I will prioritise functionality over data and data quality in future projects in order to avoid this happening again.

---
## Wins
The functions in the code snippets above illustrate the parts of this project I am most proud of. They are the functions that I found most difficult to write but presented the greatest learning opportunity and consequently helped me greatly to develop my skills further. In particular, writing more complex APIs, for example the emissions calculation is an API call that performs calculations based on user inputs.

---
## Key Learnings
I gained a much better understanding of Django’s ORM queries over the course of this project as well as its MVT architecture.

This project taught me a big lesson with regards to task prioritisation as it would have been better for us to have a more functional project with test data than a lot of valid data and a barely functional project.

In addition this project allowed me to re-familiarise myself with Python and SQL but highlighted SQL as an area that requires more practice.

---
## Bugs
As the project is incomplete I imagine there are quite a few bugs hiding in this repository however, I believe the core functionality is working correctly.

---
## Future Improvements
My ambition is to complete this project. The homepage needs additional styling, as do the recipe listing page, ingredient listing page, ingredient forms and recipe detail. Some refinement of the recipe form functionality is also required. I think the idea is great and it deserves more attention. I hope to be able to share an updated version with you soon!

---
