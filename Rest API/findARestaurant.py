import requests

def findARestaurant(food, location):
    
    #Sets the url and parameters to make the API request for restaurant information
    client_id = "Provide Your Clien ID"
    client_secret = "Provide your client secret"
    targetURL = "https://api.foursquare.com/v2/venues/search?"
    near = location
    v = "20200630"
    query = food
    
    #Adds the parameters to the URL
    targetURL += "client_id=" + client_id
    targetURL += "&client_secret=" + client_secret
    targetURL += "&near=" + near
    targetURL += "&v=" + v
    targetURL += "&query=" + query
    
    #Makes and receives the API call and turns it into a JSON object
    response = requests.get(targetURL)
    data = response.json();

    #Gets the restaurant name, address, and id from our API response object for first venues object
    if len(data['response']['venues']) == 0:
        print("No venues in " + location + " that serves " + food)
        return
    restaurant_name = data['response']['venues'][0]['name']
    restaurant_address = ""
    address_info = data['response']['venues'][0]['location']['formattedAddress']
    for i in range(len(address_info)):
        restaurant_address += address_info[i] + " "
    restaurant_id = data['response']['venues'][0]['id']
    
    #Sets the URL and adds parameters to make API request for photos
    picURL = "https://api.foursquare.com/v2/venues/"+restaurant_id+"/photos?"
    picURL += "client_id=" + client_id
    picURL += "&client_secret=" + client_secret
    picURL += "&v="+v
    
    #Makes and receives the API call and turns it into a JSON object
    picresponse = requests.get(picURL)
    picData = picresponse.json()
    
    #Get the image from our API response or set the image to a default if no pictures available
    defaultImage = "https://dummyimage.com/300.png/09f/fff"
    image = ""
    if picData['response']['photos']['count'] > 0:
        image = picData['response']['photos']['items'][0]['prefix']
        image += picData['response']['photos']['items'][0]['suffix']
    else:
        image = defaultImage
    
    #Print restaurant name, address, image
    restaurantDictionary = {'name':restaurant_name, 'address':restaurant_address, 'pic': image}
    print("Restaurant Name: " + restaurantDictionary['name'])
    print("Restaurant Address: " + restaurantDictionary['address'])
    print("Image: " + restaurantDictionary['pic'])
    return restaurantDictionary
    

#Test cases
findARestaurant("Pizza", "Tokyo, Japan")
findARestaurant("Tacos", "Jakarta, Indonesia")
findARestaurant("Tapas", "Maputo, Mozambique")
findARestaurant("Falafel", "Cairo, Egypt")
findARestaurant("Spaghetti", "New Delhi, India")
findARestaurant("Cappuccino", "Geneva, Switzerland")
findARestaurant("Sushi", "Los Angeles, California")
findARestaurant("Steak", "La Paz, Bolivia")
findARestaurant("Gyros", "Sydney, Australia")

