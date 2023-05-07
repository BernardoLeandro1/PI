from collections import Counter
import datetime
import requests
class WeatherProvider:
    def __init__(self):
        self.credential = "ed0608b1055e5035974de17e8422daab"
        self.lang = "pt"
        self.units = "metric"

    def get_weather_forecast(self, city):
        print("^^^^^^^^^^^^^^^^^^^^")
        print(city)
        print("^^^^^^^^^^^^^^^^^^^^")
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.credential}&lang=pt_br&units=metric'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract the daily forecast data from the response
        daily_forecast = []
        for forecast in data['list']:
            date_str = forecast['dt_txt'].split()[0]
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            if date not in [f['date'] for f in daily_forecast]:
                daily_forecast.append({'date': date, 'weather': []})
            daily_forecast[-1]['weather'].append(forecast)

        return daily_forecast
    
    def get_forecast_for_day(self, date, city,time=None):
        print("^^^^^^^^^^^^^^^^^^^^")
        print(city)
        print("^^^^^^^^^^^^^^^^^^^^")
        forecast = self.get_weather_forecast(city)
        for f in forecast:
            if str(f["date"]) == date:
                forecastDate = f["weather"]
                break
        
        description = []
        maxs = []
        mins = []
        for entry in forecastDate:
            maxs.append(entry["main"]["temp_max"])
            mins.append(entry["main"]["temp_min"])
            description.append(entry["weather"][0]["description"])

        maxTemp = max(maxs)
        minTemp = min(mins)
        mostCommonDescription = Counter(description).most_common()[0][0]

        #TODO melhorar frase de resposta 
        returnPhrase = "No dia "+ str(date)+" vai estar " + mostCommonDescription + "em " + city + ". Teremos máximas de " + str(maxTemp) + " graus e minimas de "+ str(minTemp) + " graus."
        """
        # Loop through forecast entries and find the closest match
        closest_forecast = None
        closest_delta = datetime.timedelta.max
        for day in forecast:
            for entry in day['weather']:
                # Get the datetime object for the forecast entry
                dt = datetime.datetime.fromtimestamp(entry['dt'])

                # Check if the weekday matches
                if dt.weekday() == weekday_num:
                    # If a specific time is specified, check if it's within the next hour
                    if time is not None:
                        time_obj = datetime.datetime.strptime(time, '%H:%M')
                        time_dt = datetime.datetime.combine(dt.date(), time_obj.time())  # combine time with date of dt
                        time_delta = time_dt - dt
                        if abs(time_delta) > datetime.timedelta(hours=1):
                            continue

                    # Calculate the delta between the forecast time and the specified time (if any)
                    if time is not None:
                        delta = abs(dt - time_dt)
                    else:
                        delta = abs(dt - datetime.datetime.now())

                    # If this forecast is closer to the specified time than the current closest forecast, update the closest forecast
                    if delta < closest_delta:
                        closest_delta = delta
                        closest_forecast = entry
        """
        return returnPhrase
    def get_forecast_for_current_day(forecast, time=None):
        if time is not None:
            # Convert time argument to datetime object
            time_obj = datetime.datetime.strptime(time, '%H:%M')
            # Get current datetime object
            current_datetime = datetime.datetime.now()

            # Combine current date with time argument to get datetime object for specified time today
            current_date = current_datetime.date()
            specified_time_today = datetime.datetime.combine(current_date, time_obj.time())

            # If specified time is in the past, add one day to current date to get the datetime object for specified time tomorrow
            if specified_time_today < current_datetime:
                specified_time_tomorrow = specified_time_today + datetime.timedelta(days=1)
                # Find the forecast for the next day
                for day in forecast:
                    if day['date'] == specified_time_tomorrow.date():
                        # Find the forecast for the closest hour to the specified time
                        closest_forecast = None
                        closest_delta = datetime.timedelta.max
                        for entry in day['weather']:
                            # Get the datetime object for the forecast entry
                            dt = datetime.datetime.fromtimestamp(entry['dt'])
                            # Calculate the delta between the forecast time and the specified time
                            delta = abs(dt - specified_time_tomorrow)
                            if delta < closest_delta:
                                closest_delta = delta
                                closest_forecast = entry
                        return closest_forecast
            else:
                # Find the forecast for today
                for day in forecast:
                    if day['date'] == current_date:
                        # Find the forecast for the closest hour to the specified time
                        closest_forecast = None
                        closest_delta = datetime.timedelta.max
                        for entry in day['weather']:
                            # Get the datetime object for the forecast entry
                            dt = datetime.datetime.fromtimestamp(entry['dt'])
                            # Calculate the delta between the forecast time and the specified time
                            delta = abs(dt - specified_time_today)
                            if delta < closest_delta:
                                closest_delta = delta
                                closest_forecast = entry
                        return closest_forecast
        else:
            # If no time is specified, return the forecast for the current hour
            current_datetime = datetime.datetime.now()
            current_hour = current_datetime.hour
            current_date = current_datetime.date()
            for day in forecast:
                if day['date'] == current_date:
                    # Find the forecast for the closest hour to the current hour
                    closest_forecast = None
                    closest_delta = datetime.timedelta.max
                    for entry in day['weather']:
                        # Get the datetime object for the forecast entry
                        dt = datetime.datetime.fromtimestamp(entry['dt'])
                        # Check if the hour matches
                        if dt.hour == current_hour:
                            delta = abs(dt - current_datetime)
                            if delta < closest_delta:
                                closest_delta = delta
                                closest_forecast = entry
                    return closest_forecast
    def get_walk_recommendation(forecast):
        # Define the thresholds for temperature, humidity, and wind speed
        temp_min = 18
        temp_max = 24
        humidity_min = 40
        humidity_max = 60
        wind_min = 10
        wind_max = 15
        # Define a function to calculate a score for a given forecast
        def calculate_score(forecast):
        # Calculate scores
            temp_score = max(0, min(1, (forecast["main"]["temp"] - temp_min) / (temp_max - temp_min)))
            humidity_score = max(0, min(1, (forecast["main"]["humidity"] - humidity_min) / (humidity_max - humidity_min)))
            if forecast["main"]["temp"] < 20:
                wind_score = max(0, min(1, (forecast["wind"]["speed"] - wind_min) / (wind_max - wind_min))) * 1.2
            else:
                wind_score = max(0, min(1, (forecast["wind"]["speed"] - wind_min) / (wind_max - wind_min))) * 0.8
        
            score = 0.5 * temp_score + 0.3 * humidity_score + 0.2 * (1 - wind_score)
            return score


        # Get the current date
        now = datetime.datetime.now()+datetime.timedelta(hours=12)

        best_score = 0
        best_forecast = None

        # Loop through the forecasts for the current day and find the best one
        for day in forecast:
            for entry in day['weather']:
            # Get the date and time of the forecast
                dt = datetime.datetime.fromtimestamp(entry["dt"])

                # Check if the forecast is for the current day
                if dt.date() == now.date():
                    # Check if the forecast is within the recommended time window
                    if dt.hour >= 10 and dt.hour <= 16:
                        # Calculate the score for the forecast
                        score = calculate_score(entry)

                        # Check if the score is better than the current best score
                        if score > best_score:
                            best_score = score
                            best_forecast = entry

        return best_forecast
