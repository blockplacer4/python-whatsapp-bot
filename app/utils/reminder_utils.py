import os
import requests
import json

from inspect import signature
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('REMINDERS_BASE_URL')
APPLICATION_ID = os.getenv('REMINDERS_APPLICATION_ID')
API_KEY = os.getenv('REMINDERS_API_KEY')

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def create_reminder(title, reminder_date, reminder_time):
    """
    Erstellt eine einmalige Erinnerung.

    :param title: Title der Erinnerung
    :param reminder_date: Datum der Erinnerung im Format 'YYYY-MM-DD'
    :param reminder_time: Uhrzeit der Erinnerung im Format 'HH:MM'
    :return: Antwort der API als JSON
    """
    data = {
        'title': title,
        'timezone': 'Europe/Berlin',
        'date_tz': reminder_date,
        'time_tz': reminder_time,
    }
    response = requests.post(f'{BASE_URL}/applications/{APPLICATION_ID}/reminders', headers=HEADERS, data=json.dumps(data))
    print()
    print(response.text)
    print()
    return response.json()

def update_reminder(reminder_id, reminder_date, reminder_time):
    """
    Aktualisiert eine bestehende Erinnerung.

    :param reminder_id: ID der zu aktualisierenden Erinnerung
    :param reminder_date: Datum der Erinnerung im Format 'YYYY-MM-DD'
    :param reminder_time: Uhrzeit der Erinnerung im Format 'HH:MM:SS'
    :return: Antwort der API als JSON
    """
    data = {}
    if reminder_time:
        data['time_tz'] = reminder_time
    if reminder_date:
        data['date_tz'] = reminder_date
    response = requests.put(f'{BASE_URL}/reminders/{reminder_id}', headers=HEADERS, data=json.dumps(data))
    return response.json()

def delete_reminder(reminder_id):
    """
    Löscht eine bestehende Erinnerung.

    :param reminder_id: ID der zu löschenden Erinnerung
    :return: Antwort der API als JSON
    """
    response = requests.delete(f'{BASE_URL}/reminders/{reminder_id}', headers=HEADERS)
    return response.json()

def get_reminders():
    """
    Ruft alle bestehenden Erinnerungen ab.

    :return: Liste der Erinnerungen als JSON
    """
    response = requests.get(f'{BASE_URL}/reminders', headers=HEADERS)
    print(response)
    return response.json()

def get_one_reminder(reminder_id):
    """
    Ruft eine bestehende Erinnerung ab.

    :return: Liste der Erinnerungen als JSON
    """
    response = requests.get(f'{BASE_URL}/reminders/{reminder_id}', headers=HEADERS)
    return response.json()

def execute_function(function_name, **kwargs):
    print("Funktion called from reminder: " + function_name)
    print("Args gave within reminders: " + str(kwargs))
    functions = {
        'create_reminder': create_reminder,
        'update_reminder': update_reminder,
        'delete_reminder': delete_reminder,
        'get_reminders': get_reminders,
        'get_one_reminder': get_one_reminder
    }
    if function_name in functions:
        func = functions[function_name]
        func_params = signature(func).parameters
        filtered_kwargs = {key: kwargs[key] for key in func_params if key in kwargs}
        return func(**filtered_kwargs)
    else:
        raise ValueError(f"Function '{function_name}' not found.")


