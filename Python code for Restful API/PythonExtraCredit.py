'''
Travis Chen - Extra Credit Coding Assignment

Create a python application that takes an input request of a city and displays 
the current weather for that city. Based on the temperature returned determine if the 
user making input should wear a coat (a temperature of 65 degrees or lower) or if they
are safe to wear shorts ( a temperature of 66 degrees of higher).

For this example you will need to use the following api key c8efac34cc3548754ca009222d24da49
to interact with the openweather api.

The base url required for these api calls : http://api.openweathermap.org/data/2.5/weather?

The fully quantified api/url will be the base url + "appid=c8efac34cc3548754ca009222d24da49&q=" + city_entered

Hints:

https://openweathermap.org/current#cityid

Your python application will require "requests" and "json" (feel free to use any others!)

Conversion to Fahrenheit might be required

Please upload your python code in the form of a .py file and screenshot(s) of the output of your code.
 
Extra Credit Points Determined by the following:
1D Point for even attempting
1D Point for successful API call
1D point for parsing the data 
1D point for conditional implementation ( wear a coat/ wear shorts)
1D point for correct output decision


a copy of the json output for helping my code
used https://jsonformatter.curiousconcept.com/ to help with formatting since it was not formatted from my terminal

{
   "coord":{
      "lon":-92.4053,
      "lat":44.1078
   },
   "weather":[
      {
         "id":800,
         "main":"Clear",
         "description":"clear sky",
         "icon":"01n"
      }
   ],
   "base":"stations",
   "main":{
      "temp":297.54,
      "feels_like":297.84,
      "temp_min":294.85,
      "temp_max":298.96,
      "pressure":1015,
      "humidity":69
   },
   "visibility":10000,
   "wind":{
      "speed":1.54,
      "deg":110
   },
   "clouds":{
      "all":0
   },
   "dt":1657247521,
   "sys":{
      "type":1,
      "id":3199,
      "country":"US",
      "sunrise":1657190031,
      "sunset":1657245291
   },
   "timezone":-18000,
   "id":0,
   "name":"Rochester",
   "cod":200
'''
import requests, re 

#whatToWear will tell if whether to  wear a coatr if the temp is below 65 degree, wear sh ots if temp is above 66
#Fahenheint in as int and will  print statement based on temperature given
def whatToWear(temp):
    if temp <= 64:
        print("Its chilly! Make sure to bring a coat")
    if temp > 66:
        print("The weather is nice enough to wear shorts!")

#takes in zip codes as input to retrieve the weather from opweathermap's API. Weather will be returned in fahrenheit as a json
def get_weather(zip):
    #Defined Variables
    apiKey  = "REDACTED" #key to use api (Provided by FS)
    apiKey2 = "REDACTED" #Personal API key 
    apiCall = "http://api.openweathermap.org/data/2.5/weather?" #base url for requesting weather
    units   = 'imperial' #change the value of the unit return from API (Choose from standard, metric, imperial)

    #call open weather to get weather information
    get_weather = requests.get(apiCall + 'zip=' + str(zip) + "&appid=" + apiKey + "&units=" + units)
    data = get_weather.json()

    #get temp from json returned form openweather api
    temp = data['main'].get('temp')
    print("Town: ", data['name'])
    #debug code to see the json out and check what call is being made
    if __name__ == '__main__':
        print("------API call----")
        print(apiCall + 'zip=' + str(zip) + "&appid=" + apiKey)
        print("----- raw JSON OUT----------")
        print(data)
        print("-----------------------")
    return temp

#takes a input int in from user and validates that it is 5 digits
def get_zip():
    try:
        zip = str(input("Please enter a zipcode \n"))
        check = re.search('\d{5}', zip)
        if (check):
            return zip
        else:
            print("please check zip code")
            return 0
    except:
        print("Please check your zip code")
        return 0

def main(): 
    zip = get_zip()
    if zip != 0:
        try:
            print("Getting Temperature...")
            temp = get_weather(zip)
            print("Temperature is: ", temp)
            whatToWear(temp)
        except:
            pass
    if zip == 0:
        print("There was a problem with the zip code given")
main()
