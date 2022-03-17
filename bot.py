import telebot
import requests 
bot=telebot.TeleBot('HERE YOU PASTE YOUR TELEGRAM BOT TOKEN')

#we call bot, tell him what he must do after command 
@bot.message_handler(commands=['start']) 
def send_start(message): #creat fun
    bot.reply_to(message, "Enter city name")

#what he must do after user send city name 
@bot.message_handler(content_types=['text'])
def send_message(message):
    BASE_URL="http://api.openweathermap.org/data/2.5/weather"
    API_KEY = "YOUR API KEY"
    #here we connect to api weather
    city = message.text #m.text is m. which user send
    requests_url= f"{BASE_URL}?appid={API_KEY}&q={city}"
    response=requests.get(requests_url)

    if response.status_code==200: 
        data=response.json()

        weather=data['weather'][0]['description']
        if 'clouds' in weather:
            weather1=f'Weather is: {weather}☁️'
        elif 'sun' in weather:
            weather1=f'Weather is: {weather}☀️'
        elif 'rain' in weather:
            weather1=f'Weather is: {weather}🌧 (I think you should take an ubrella☔)'
        else:
            weather1=f'Weather is: {weather}'
            
        
        temperature=round(data["main"]['temp'] - 273.15, 1)
        if temperature < -20:
            temperature1=f'\nOh fuck temperature is {temperature}°С this is very fucking cold! You should stay home if you want to survive 💀'
        elif temperature < -5:
            temperature1=f'\nt: {temperature}°С (it seems to me that you should dress warmer🥶)'
        elif temperature > 25:
            temperature1=f"\nt: {temperature} (I've always hated the heat🤬)"
        else:
            temperature1=f'\nt: {temperature}°С'

        pressure=data['main']['pressure']
        pressure1=f'\npressure: {pressure}mb'

        wind_sp=data['wind']['speed']
        wind_sp1=f'\nwind speed: {wind_sp} m/s'

        humidity=data['main']['humidity']
        humidity1=f'\nair humidity: {humidity}%'

        vis=data['visibility'] / 1000
        if vis >= 10:
            visibility=f"\nvisibility: {vis}km (well, it's great weather to exterminate russian solders using your rifle)"
        else:
            visibility=f'\nvisibility: {vis}km'

        #creat, send message
        weather_all=weather1+temperature1+pressure1+wind_sp1+humidity1+visibility
        bot.send_message(message.chat.id, weather_all)

    else:
        bot.send_message(message.chat.id, "Sorry I don't have any information about this city. It seems to me that you live in real ass of the hole world")

bot.infinity_polling() #start bot