# importing required modules/libraries
import requests
import random
import urllib.request
import json
import requests
import colorama
colorama.init()


def choose():  # main-menu function
    print("\033[36m--------------------------Welcome To AgriBot 2.0!--------------------------\n Please enter:")
    print("\033[31m1 If you want to see which plants you can grow as per your soil's pH and city's temperature")
    print("\033[32m2 If you want to learn if your soil contains harmful chemicals")
    print("\033[33m3 If you want to take an educational quiz")
    print("\033[34m4 If you want to explore the Trefle API")
    print("\033[35m5 If you want alternatives to NPK fertiliser")
    print("\033[37m6 If you want to get your soil's pH to that required by your plant\n")
    choice = input()
    if choice == "1":  # statements used to call relevant funtions
        weather()
    elif choice == "2":
        chemamt()
    elif choice == "3":
        quiz()
    elif choice == "4":
        data = field()
        odata = searchcrit(data)
        output(odata)
    elif choice == "5":
        fertalt()
    elif choice == "6":
        optimiseph()
    elif choice == "":
        return
    else:
        print("Please enter a valid value, if you want to exit please press ENTER\n")
        choose()


def weather():  # function to get the weather of a city
    city = input("\n\033[32mEnter your city:\n")
    pH = float(input("\n\033[31mEnter your soil's pH:\n"))
    print()
    pH2 = round(pH, 1)
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather/?"
    API_KEY = "acec9d7157da71db5c1cfd7af406e564"
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city  # making sure the url is formatted properly
    response = requests.get(url).json()  # accessing the weather API
    tempkelvin = response['main']['temp']  # isolating the temperature from the data received from the API
    tempcelsius = tempkelvin - 273.15
    tempfahrenheit = tempcelsius * (9 / 5) + 32
    tempfahrenheit2 = round(tempfahrenheit, 0)
    apiurl(tempfahrenheit2, pH2)


def apiurl(temp, ph):  # function to access the table where all the data about plant species is stored
    base_url = "https://api.airtable.com/v0/appDqoT5WqXO66TWQ/"
    if temp < 32 or temp > 113:  # making sure temperature is in the proper range
        if temp < 32:
            print("Tempertaure too low.\n")
        else:
            print("Temperature too high.\n")
        print("You can try a different temp between 32-113(°F) if you have a controlled setup\n")
        print("Or press ENTER to exit:")
        temp = input()
        if temp == "":
            return
        temp = int(temp)
        if temp < 32 or temp > 113:
            apiurl(temp, ph)
    if ph < 4.5 or ph > 8.4:  # making sure that the pH is in the proper range
        if ph < 4.5 and ph >= 0:
            print("pH too low")
        elif ph > 8.4 and ph <= 14:
            print("pH too high")
        elif ph > 14 or ph < 0:
            print("Please enter a valid value")
        print('check funtion 6 if you need help fixing pH')
        return
    else:
        if ph >= 4.5 and ph <= 5:  # if both temp and pH are in proper range, 
        #these statements are used to format the url
            halfurl = base_url + "pH (4.5-5), "
        elif ph >= 5.1 and ph <= 5.5:
            halfurl = base_url + "pH (5.1-5.5), "
        elif ph >= 5.6 and ph <= 6:
            halfurl = base_url + "pH (5.6-6), "
        elif ph >= 6.1 and ph <= 6.5:
            halfurl = base_url + "pH (6.1-6.5), "
        elif ph >= 6.6 and ph <= 7.3:
            halfurl = base_url + "pH (6.6-7.3), "
        elif ph >= 7.4 and ph <= 7.8:
            halfurl = base_url + "pH (7.4-7.8), "
        elif ph >= 7.9 and ph <= 8.4:
            halfurl = base_url + "pH (7.9-8.4), "
        if temp >= 32 and temp <= 50:
            fullurl = halfurl + "Temperature (32-50 F)"
        elif temp >= 51 and temp <= 76:
            fullurl = halfurl + "Temperature (51-76 F)"
        elif temp >= 77 and temp <= 92:
            fullurl = halfurl + "Temperature (77-92 F)"
        elif temp >= 93 and temp <= 108:
            fullurl = halfurl + "Temperature (93-108 F)"
        elif temp >= 109 and temp <= 113:
            fullurl = halfurl + "Temperature (109-113 F)"
    printdata(fullurl)


def printdata(fullurl):  # function to retrieve data from url
    lst = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m"]
    auth_token = "patxQaeu7laOYD3kQ.b0ee1734ef0de3d012614d66cb2f0681665120e922e07567674192d7dc8a2eb2"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(fullurl, headers=headers)  # retrieves data from air table
    data = response.json()
    FullString = ""
    Plant = ""
    count = 0
    for i in range(len(data['records'])):  # nested loop is used to print data out in proper format
        for k, v in (data['records'][i]['fields']).items():
            if k != "Visual":
                if k == "Plants":
                    Plant = str(i + 1) + ". " + v + ":" + "\n"
                else:
                    FullString = FullString + k + ": " + v + "\n"
        print(lst[count] + Plant + FullString)
        FullString = ""
        if count < 6:
            count = count + 1
        else:
            count = 0
    k = input("Press ENTER to exit, or SPACE and then ENTER to go back to the main program")
    if k == " ":
        choose()  # recursive call to the main function


def fertalt():  # function to find alternatives for NPK fertilizers
    k = ""
    fert = input("Press N for Nitrogen, P for Phosphorus, and K for Potassium for alternates:\n")
    if fert.lower() == "n":
        print("\033[31m Nitrogen requirement can be fulfilled through coffee grounds, blood meal, and cotton seed meal.")
    elif fert.lower() == "p":
        print("\033[32m Phosphorus requirement can be fulfilled through fish bone meal, steamed bone meal, and rock dust.")
    elif fert.lower() == "k":
        print(" \033[33m Potassium requirement can be fulfilled through kelp meal, hardwood ash, and green organic material.")
    k = input("\nPlease enter either R to repeat, ENTER to exit or SPACE to go back to main program.\n")
    if k.lower() == "r":
        fertalt()
    if k == " ":
        choose()


def optimiseph():  # function to figure out how to lower or increase pH to required levels
    print("\n\033[31mTo increase pH-use hydrated limestone or woodash, 0.5 lbs every ten square foot to increase pH by one point.")
    print("\033[34mTo lower pH-through natural acidifiers (manure/compost), or chemicals like aluminium sulfate or iron sulphate.\n")
    k = input("\n\033[37mPress ENTER to exit, or SPACE and then ENTER to go back to the main program")
    if k == " ":
        choose()


def chemamt():  # function used to find toxic chemicals in soil
    print("\nHere's a list of chemicals you should looks out for if your plants aren't growing as they should be:\n")
    d = {"Heavy Metals": ["Lead", "Cadmium", "Mercury"], "Excess Salts": ["Sodium", "Chlorine"],
         "Air Pollutants": ["Ozone (O3)", "Sulfur Dioxide (SO2)", "Nitrogen Dioxide (NO2)"],
         "Pesticides/Herbicides": ["Glyphosate", "DDT"], "Petroleum Products": ["Oil", "Diesel"],
         "Acids": ["Sulfuric Acid", "Nitric acid"], "Alkalis": ["Sodium Hydroxide", "Potassium Hydroxide"]}
    #dictionary of harmful chemicals in soil
    for i in d:  # loop used to print data from the dictionary in an orderly manner
        print(i + ":")
        for j in d[i]:
            print("     " + j)
    print("\nYou can also just input chemicals you are worried about (seperated by a comma) and we'll do the work")
    chem = input("Input the chemicals you want to check, alternatively you can ignore by pressing ENTER.\n")
    if chem == "":
        return
    lst = chem.split(",")
    output = []
    for i in lst:  # nested loop used to figure out what harmful chemicals the user has in their soil
        for j in d:
            for k in d[j]:
                if i.lower() == k.lower():
                    if j == "Excess Salts" or j == "Air Pollutants":
                        output.append(i + " -Harmful in excess")  # adds warning that these chemicals are only harmful in excess
                    else:
                        output.append(i)  # appends harmful chemicals to a list
    if output == []:
        print("\033[34mNo harmful chemicals were found in your soil")
    else:
        print("\033[31mThese are the harmful chemicals found in your soil:")
        for i in output:  # prints the list of harmful chemicals found in the users soil
            print("   " + i)
    k = input("\nPress ENTER to exit, or SPACE and then ENTER to go back to the main program.")
    if k == " ":
        choose()


def quiz():
    lstt = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m"]
    countt = 0
    myFile = open("Questions.txt", mode="r")  # used to open file where questions and answers for quiz are stored
    s = "123"  # temp data
    points = 0
    lst = []
    qord = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]  # list used to ensure that questions given to user are in random order
    correct = []
    random.shuffle(qord)  # shuffling questions
    while s != "":  # loop used to read each line of the file and seperate it
    #into a nested list in the format [Question,MCQ's,Answer]
        s = myFile.readline()
        s = s.strip()
        lst.append(s.split("//"))
    lst.remove([''])

    for i in range(0, len(lst)):
        temp = lst[i][2].split(",")  # used to spilt the answers
        lst[i][2] = temp
        temp = lst[i][1].split(",")  # used to spilt the mcq statements
        random.shuffle(temp)  # used to shuffle the statement list
        lst[i][1] = temp

    for i in range(0, 5):  # used to print the question and statements
        ans_flag = False
        count = 1
        print(lstt[countt] + lst[qord[i]][0])  # printing questions
        for j in lst[qord[i]][1]:  # printing MCQ statements
            print("     " + str(count) + ". " + j)
            count += 1
        temp = int(input())
        ans = lst[qord[i]][1][temp - 1]  # getting answer list
        for k in lst[qord[i]][2]:  # figuring out if the user answered correctly or not
            if ans == k:
                ans_flag = True
        correct.append([qord[i], ans, ans_flag])  # appending the data to list to be used late
        if ans_flag == True:
            points += 1  # adding points
        countt += 1

    print()

    if points == 0:
        print("\033[34mCongrats you got 0 answers correct!! Did you even try?")
    else:
        print("\033[34mCongrats you got " + str(points) + " answers correct!!")  # printing score
    print("\033[33mFor reference, here's the questions and their respective answers to learn from")
    for i in correct:  # loop used to print question, the users answer,
        #and what the answer should be
        pos = i[0]
        print("\033[32m\nThe question was:\n" + lst[pos][0])
        print("\033[31m\nYour answer was:\n" + i[1])
        if i[2] == True:
            print("\n\033[34mYou got this answer: Right")
        else:
            print(("\n\033[31mYou got this answer: Wrong"))
            print("\n\033[35mThe correct answer was:\n" + lst[pos][2][0])
    myFile.close()
    k = input("\nPress ENTER to exit, or SPACE and then ENTER to go back to the main program")
    if k == " ":
        choose()


def searchcrit(field):  # function used to access trefle API
    output = []
    token = "token=jI2LbWw-6CmNAW9DZpVzrxPPxNau8irx2Usajh22jkw&"
    with urllib.request.urlopen("https://trefle.io/api/v1/plants?" + token + field) as response:
        data = response.read()

    d = json.loads(data)
    output += d["data"]  # isolating plant data from recieved response
    total = d['meta']

    total = total['total']
    pages = total // 30  # figuring out the num of plants that should be printed
    if pages > 10:
        pages = 10

    for i in range(2, pages + 1):  # loop used to access the next pages of the API and append it into the output list
        with urllib.request.urlopen("https://trefle.io/api/v1/plants?" + token + field + "&page=" + str(i)) as response:
            data = response.read()
            d = json.loads(data)
            output += d["data"]

    return output


def output(data):  # function used to output data recieved from trefle
    lst = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m"]
    countt = 0
    print("Based on your input parameters, here are some plants you can grow:")
    count = 1
    for i in data:
        print()
        if i['common_name'] == None:
            i['common_name'] = "[None]"  # making sure code doesn't crash from trying to output null data 
        if i['scientific_name'] == None:
            i['scientific_name'] = "[None]"
        print(lst[countt] + str(count) + ". " + i['common_name'] + " also scientifically known as, " + i['scientific_name'])
        if countt < 6:
            countt += 1
        else:
            countt = 0
        count += 1
    k = input("\nPress ENTER to exit, or SPACE and then ENTER to go back to the main program.")
    if k == " ":
        choose()


def field():  # function used to take input from user for the sorting parameter
    #dictionary of sorting options available to the user:
    d = {1: "&range[ph_minimum]=", 2: "&filter_not[edible_parts]=null", 3: "&range[maximum_height]=", 4: "&range[light]="}
    print("\033[32mWe have 5 parameters to sort plants on")
    print("\033[33m1.pH")
    print("\033[34m2.Edible Plants")
    print("\033[35m3.Height")
    print("\033[36m4.Amount of light")
    print("\033[37m5.None")
    num = input("Please enter the parameter you would like the plants to be sorted on, or press ENTER to exit: ")
    if num not in "12345":  # validation checks
        while num not in "12345" or num != "":
            print("\nPlease input a valid value,")
            num = input()
    if num == "":
        return

    field = ""

    num = int(num)
    if num == 1:  # series of conditional statements used to format the url properly for each sorting parameter
        pH = int(input("\nPlease input an your soil's pH value: "))
        if pH == 1:  # ensuring edge cases are accounted for
            pH += 1
        elif pH == 14:
            pH += -1
        field = d[1] + str(pH - 1) + "," + str(pH + 1)  # converting a single value into a range
    elif num == 2:
        field = d[2]
    elif num == 3:
        print("\nPlease input the height, in cm, you want your plants to be")
        print("If you want your plants to be taller than a certain height, enter that height like this 'x,'")
        print("If you want your plants to be shorter than a certain height, enter that height like this ',x'")
        height = input()
        field = d[3] + height
    elif num == 4:
        print("\nPlease enter a light value on a scale of 1-10, 1 being next to no direct light, and 10 being intense light")
        light = int(input())
        if light == 1:  # ensuring edge cases
            light += 1
        elif light == 10:
            light += -1
        field = d[4] + str(light - 1) + "," + str(light + 1)

    return (field + "&&filter_not[common_name]=null")  # returning the parameter on which the data will be sorted

choose()
