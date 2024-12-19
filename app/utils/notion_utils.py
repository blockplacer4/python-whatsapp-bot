import os
from dotenv import load_dotenv
from notion_client import Client
from flask import current_app, jsonify

load_dotenv()
notion = Client(auth=os.getenv('NOTION_TOKEN'))

def get_all_pages(database_id):
    """
    Holt alle Seiten einer angegebenen Notion-Datenbank ab, die nicht den Status "Erledigt" haben.

    Args:
        database_id (str): Die ID der Notion-Datenbank

    Returns:
        list: Eine Liste der formatierten Seiten
    """
    try:
        response = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "Status",
                "status": {
                    "does_not_equal": "Erledigt"
                }
            }
        )
        return format_pages(response.get("results", []))
    except Exception as e:
        print(f"Fehler beim Abrufen der Seiten: {e}")
        return None

def format_pages(pages):
    """
    Formatiert die Seiten in ein lesbares Format.

    Args:
        pages (list): Eine Liste von Seiten aus der Notion-API

    Returns:
        list: Eine Liste von formatierten Seiten
    """
    formatted = []
    for page in pages:
        properties = page.get("properties", {})
        formatted_page = {
            "Aufgabe": extract_plain_text(properties.get("Aufgabe", {}).get("title", [])),
            "Fach": properties.get("Fach", {}).get("select", {}).get("name", ""),
            "Deadline": properties.get("Deadline", {}).get("date", {}).get("start", ""),
            "Status": properties.get("Status", {}).get("status", {}).get("name", "")
        }
        formatted.append(formatted_page)
    return formatted

def extract_plain_text(title_objects):
    """
    Extrahiert den Klartext aus den Titel-Objekten einer Notion-Seite.

    Args:
        title_objects (list): Eine Liste von Titel-Objekten

    Returns:
        str: Der extrahierte Klartext
    """
    return "".join([obj.get("text", {}).get("content", "") for obj in title_objects])

def create_page(database_id, properties):
    """
    Erstellt eine neue Seite in einer angegebenen Notion-Datenbank.

    Args:
        database_id (str): Die ID der Notion-Datenbank
        properties (dict): Die Eigenschaften der neuen Seite

    Returns:
        dict: Die Antwort der Notion-API nach der Erstellung der Seite
    """
    try:
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
        return response
    except Exception as e:
        print(f"Fehler beim Erstellen der Seite: {e}")
        return None