import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('REMINDERS_BASE_URL')
APPLICATION_ID = os.getenv('REMINDERS_APPLICATION_ID')
API_KEY = os.getenv('REMINDERS_API_KEY')

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def create_reminder(title, reminder_date, reminder_time, rrule=None):
    """
    Erstellt eine einmalige Erinnerung.

    :param title: Title der Erinnerung
    :param reminder_date: Datum der Erinnerung im Format 'YYYY-MM-DD'
    :param reminder_time: Uhrzeit der Erinnerung im Format 'HH:MM:SS'
    :param rrule: Recursion rule | Example: Every 2 years, in July and December on the last Thursday: FREQ=YEARLY;INTERVAL=2;BYMONTH=7,12;BYDAY=-1TH | Example 2: Every 2 weeks, on Monday, Wednesday, and Friday: FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,WE,FR
    :return: Antwort der API als JSON
    """
    data = {
        'title': title,
        'date_tz': reminder_date,
        'time_tz': reminder_time,
        'rrule': rrule
    }
    response = requests.post(f'{BASE_URL}/applications/{APPLICATION_ID}/reminders', headers=HEADERS, data=json.dumps(data))
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
    return response.json()

def get_one_reminder(reminder_id):
    """
    Ruft eine bestehende Erinnerung ab.

    :return: Liste der Erinnerungen als JSON
    """
    response = requests.get(f'{BASE_URL}/reminders/{reminder_id}', headers=HEADERS)
    return response.json()

