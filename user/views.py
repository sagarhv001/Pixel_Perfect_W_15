from django.shortcuts import render,redirect,HttpResponse
from user.models import *
from user.models import User_Details, User_History, User_Goal
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date
import pandas as pd
import joblib

# Create your views here.
def index(request):
    if 'email' in request.session:
        user_data = User_Details.objects.get(email = request.session['email'])
       
        return render(request, 'index.html',{'user_data': user_data})
    else:
        return render(request, 'index.html')

def register(request):
    global c_otp
    # when we click on register option
    if request.method == 'GET':
        return render(request, 'register.html')
    
    # when we click on register button
    else:
       
        # checking whether the entered email is already used for registration
        try:
            # error occurs when there is no email match
            # then control goes to except block

            global user_details 
            user_details=User_Details.objects.get(email = request.POST['email'])
            return render(request,'register.html',{'msg':"Email already registered, try using other Email"})
        
        except:
            # validating password and confirm password
            if request.POST['password'] == request.POST['confirmpassword']:
                #  generating otp
                global c_otp
                c_otp = randint(100_000,999_999)

                #extracting data from registration form
                global reg_form_data 

                reg_form_data = {
                    "name" : request.POST['name'],
                    "email" : request.POST['email'],
                    "password" : request.POST['password'],
                    "confirmpassword" : request.POST['confirmpassword']
                    
                }

                # sending the generated OTP via mail
                subject = "OTP Verification"
                message = f'Hello{reg_form_data["name"]}, Welcome to Pixel Perfect. Your OTP is {c_otp}'
                sender = settings.EMAIL_HOST_USER
                receiver = [reg_form_data['email']]
                send_mail(subject, message, sender, receiver)

                #after sending OTP render the page to enter OTP
                return render(request,'otp.html')

            else:
                return render(request, 'register.html',{'msg':"Both Passwords didn't match"})
            
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            # finding the record of person trying to login in database
            session_user = User_Details.objects.get(email = request.POST['email'])
            if request.POST['password'] == session_user.password:
                request.session['email'] = session_user.email

                # Code to add 5 points
                session_user.points += 5
                session_user.save()
                
                # Display message 
                messages.success(request, '5 points added to your account for logging in!')
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg':'invalid password'})
        except:
            return render(request, 'login.html',{'msg': 'This email is not Registered !!'})

def about(request):
    if 'email' in request.session:
        user_data = User_Details.objects.get(email = request.session['email'])
       
        return render(request, 'about.html',{'user_data': user_data})
    else:
        return render(request, 'about.html')


def contact(request):
    if 'email' in request.session:
        user_data = User_Details.objects.get(email = request.session['email'])
       
        return render(request, 'contact.html',{'user_data': user_data})
    else:
        return render(request, 'contact.html')


def calculator(request):
    if 'email' in request.session:
        user_data = User_Details.objects.get(email = request.session['email'])
       
        return render(request, 'calculator.html',{'user_data': user_data})
    else:
        return render(request, 'calculator.html')


def otp(request):
    if str(c_otp) == request.POST['u_otp']:
        User_Details.objects.create(name=reg_form_data['name'], email = reg_form_data['email'],password = reg_form_data['password'])
        return render(request,'register.html', {'msg': "Registration Successfull !! Account created"})
    else:
        return render(request, 'otp.html',{'msg':"Invalid OTP"})


def discover(request):
    if 'email' in request.session:
        user_data = User_Details.objects.get(email = request.session['email'])
       
        return render(request, 'discover.html',{'user_data': user_data})
    else:
        return render(request, 'discover.html')



def logout(request):
    del request.session['email']
    return redirect('index')

def challenges(request):
    if 'email' in request.session:
        user_data = User_Details.objects.get(email = request.session['email'])
       
        return render(request, 'challenges.html',{'user_data': user_data})
    else:
        return render(request, 'challenges.html')


def calculate_carbon_emission(request):

    # extracting data from form
    electricity_usage =int(request.POST['electricityUsage']) 
    oil_usage = int(request.POST['oilUsage'])
    gas_usage = int(request.POST['gasUsage'])
    lpg_usage = int(request.POST['lpgUsage'])

    transport_mode = request.POST['transportMode']
    vehicle_mileage = int(request.POST['vehicleMileage'])
    vehicle_cc = int(request.POST['vehicleCC'])
    distance_travelled= int(request.POST['distanceTravelled'])

    meat_eater= request.POST['meatEater']
    meals_per_day=int(request.POST['mealsPerDay'])


    appliance_hours = int(request.POST['totalApplianceHours'])
    appliance_usage = int(request.POST['applianceUsage'])
    water_consumption = int(request.POST['waterConsumption'])
    waste_produced = int(request.POST['wasteProduced'])



    electricity_emission_factor = 0.5  # Emission factor for electricity usage
    oil_emission_factor = 2.3  # Emission factor for oil usage
    gas_emission_factor = 1.9  # Emission factor for gas usage
    lpg_emission_factor = 1.5  # Emission factor for LPG usage
    vehicle_emission_factor = 2.0  # Average emission factor for vehicle


    energy_emission = (electricity_usage * electricity_emission_factor +
                      oil_usage * oil_emission_factor +
                      gas_usage * gas_emission_factor +
                      lpg_usage * lpg_emission_factor)

    travel_emission = 0
    food_emission = 0
    appliance_emission = 0
    water_emission = 0

    if transport_mode == 'car':
        travel_emission += vehicle_mileage * vehicle_emission_factor + (vehicle_cc / 1000)  # Adjust for vehicle CC
    elif transport_mode == 'publicTransport':
        travel_emission += distance_travelled * 0.5  # Emission factor for public transport
    elif transport_mode == 'bicycle':
        travel_emission += 0  # No emissions for bicycle

    if meat_eater == 'Yes':
        food_emission += meals_per_day * 3  # Emission factor for meat eater
        
    appliance_coefficient = 0.02  # tons of CO2 per unit of energy efficiency score
    water_coefficient = 0.001  # tons of CO2 per liter of water consumed
    waste_coefficient = 0.05  # tons of CO2 per kg of waste produced
    appliance_emission = appliance_coefficient * float(appliance_usage) * float(appliance_hours)  # converting tons to kilograms
    water_emission = water_coefficient * float(water_consumption)  # converting tons to kilograms
    waste_emission = waste_coefficient * float(waste_produced)  # converting tons to kilograms
    global carbon_emission
    carbon_emission = {'energy_emission':energy_emission, 'travel_emission':travel_emission,'food_emission': food_emission,'appliance_emission': appliance_emission,'waste_emission':waste_emission,'water_emission': water_emission} 
    daily_emission = energy_emission + travel_emission + food_emission + appliance_emission + water_emission + waste_emission

    #extracting userdata
    user_data = User_Details.objects.get(email = request.session['email'])

    if 'email' in request.session:
    #pushing data to database
        User_History.objects.create(email = user_data, date=date.today(),food_emsn=food_emission,travel_emsn=travel_emission,energy_emission=energy_emission,appliance_emission=appliance_emission,water_emission=water_emission,waste_emission=waste_emission,daily_emsn=daily_emission)
        


    msg2=carbon_footprint(request,carbon_emission)
    return render(request, 'calculator.html',{'msg1':"Your total Carbon emission is: "+str(round(daily_emission,2))+"KgCO2",'msg2':msg2, 'user_data': user_data})



def dashboard(request,):
    if 'email' in request.session:
        user_data = User_Details.objects.get(email = request.session['email'])
        user_history = User_History.objects.filter(email = user_data).order_by('-date')

        return render(request, 'dashboard.html',{'user_data':user_data,'user_history':user_history})
    else:
        return render(request, '.html')
    
def carbon_footprint(request,carbon_emission):
    import pandas as pd
    import time

    # Assuming the 'carbon_footprint' column represents the target variable
    # Replace the following line with the path to your CSV file
    # file_path = 'E:\desktop\recmd\dataset_with_avg_values.csv'
    data = pd.read_csv("data\dataset_with_avg_values.csv") 
    X = data.iloc[:, [2, 3, 4, 5, 6, 7]]  # Add columns for daily water emission and daily appliances emission
    y = data.iloc[:, -1]   # Target variable is the last column

    # Train a linear regression model


    # Hardcoded threshold values
    threshold_values = {'Daily Travel Emission': 2.80, 'Daily Energy Emission': 11.16, 'Daily Dietary Emission': 6.46,
                        'Daily Waste Emission': 3.03, 'Daily Water Emission': 5.0, 'Daily Appliances Emission': 8.0}

    # User input for daily emissions
    daily_travel_emission =carbon_emission['travel_emission']
    daily_energy_emission = carbon_emission['energy_emission']
    daily_dietary_emission = carbon_emission['food_emission']
    daily_waste_emission = carbon_emission['waste_emission']
    daily_water_emission = carbon_emission['water_emission']
    daily_appliances_emission = carbon_emission['appliance_emission']

    # Calculate the ratio of user input to threshold values
    ratio = pd.Series({
        'Daily Travel Emission': daily_travel_emission / threshold_values['Daily Travel Emission'],
        'Daily Energy Emission': daily_energy_emission / threshold_values['Daily Energy Emission'],
        'Daily Dietary Emission': daily_dietary_emission / threshold_values['Daily Dietary Emission'],
        'Daily Waste Emission': daily_waste_emission / threshold_values['Daily Waste Emission'],
        'Daily Water Emission': daily_water_emission / threshold_values['Daily Water Emission'],
        'Daily Appliances Emission': daily_appliances_emission / threshold_values['Daily Appliances Emission']
    })

    # Get the attributes with abnormally high ratios
    abnormally_high_attributes = ratio[ratio > 1.0]

    # Generate recommendation based on the user input
    if len(abnormally_high_attributes) == 0:
        print("Analyzing your carbon footprint...")
        time.sleep(2)
        recommendation_message = "Your carbon footprint is within sustainable limits. Great job! 🌱"
    else:
        # Build recommendation messages for each abnormally high attribute
        print("Analyzing your carbon footprint...")
        time.sleep(2)
        recommendation_messages = []
        for attribute, value in abnormally_high_attributes.items():
            times_above_threshold = round(value, 2)
            recommendation_messages.append(
                f"Your {attribute} is {times_above_threshold} times higher than the suggested average. 📈\n"
                f"Consider the following recommendations to reduce your {attribute}:\n"
            )
            # Specific recommendations for each attribute
            if attribute == 'Daily Travel Emission':
                recommendation_messages.extend([
                    "1. Use Sustainable Transportation: Encourage walking, cycling, carpooling, or using public transportation.",
                    "2. Telecommuting: If feasible, promote remote work or telecommuting options.",
                    "3. Optimize Routes: Plan and optimize travel routes to minimize distance and fuel consumption. 🚴‍♂🌍"
                ])
            elif attribute == 'Daily Energy Emission':
                recommendation_messages.extend([
                    "1. Energy-Efficient Appliances: Promote the use of energy-efficient appliances.",
                    "2. Renewable Energy Sources: Advocate for the use of renewable energy sources.",
                    "3. Power Down Devices: Turn off lights, electronics, and other devices when not in use. 💡🌞"
                ])
            elif attribute == 'Daily Dietary Emission':
                recommendation_messages.extend([
                    "1. Plant-Based Diet: Promote a plant-based diet with more fruits, vegetables, and plant-based proteins.",
                    "2. Local and Seasonal Produce: Choose locally sourced and seasonal produce.",
                    "3. Reduce Food Waste: Plan meals, store food properly, and compost organic waste. 🥦🌽"
                ])
            elif attribute == 'Daily Waste Emission':
                recommendation_messages.extend([
                    "1. Recycling and Composting: Encourage recycling and composting.",
                    "2. Reduce Single-Use Items: Advocate for the reduction of single-use items.",
                    "3. Educate on Proper Disposal: Provide information on proper waste disposal methods. ♻🗑"
                ])
            elif attribute == 'Daily Water Emission':
                recommendation_messages.extend([
                    "1. Water Conservation: Adopt water-saving practices like fixing leaks and using low-flow appliances.",
                    "2. Responsibly Landscape: Implement landscaping practices that conserve water.",
                    "3. Educate on Water Footprint: Inform about the water footprint of different products. 💧🌿"
                ])
            elif attribute == 'Daily Appliances Emission':
                recommendation_messages.extend([
                    "1. Energy Star Appliances: Use energy-efficient appliances with the Energy Star label.",
                    "2. Smart Home Technology: Promote the use of smart home technology to optimize energy usage.",
                    "3. Regular Maintenance: Perform regular maintenance on appliances for optimal efficiency. 🏡🔧"
                ])

        # Combine recommendation messages
        recommendation_message = "\n\n".join(recommendation_messages)

    # Display recommendation with delays, colors, and emojis
    print("Generating personalized recommendations...")
    time.sleep(3)
    print("Your Carbon Footprint Recommendation:")
    return (recommendation_message)


def saveChallenge(request):
    if request.method == 'POST':
        User_Goal.objects.create(gl_travel_emsn = request.POST['travel'],gl_energy_emsn =request.POST['travel'],gl_food_emsn=request.POST['travel'],gl_water_emsn=request.POST['travel'], gl_waste_emsn=request.POST['travel'],gl_appliance_emsn=request.POST['travel'],gl_daily_emsn=request.POST['travel'] )
        
    return redirect('index')
