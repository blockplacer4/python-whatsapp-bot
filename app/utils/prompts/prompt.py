from datetime import datetime

def replace_placeholders(file_path, notion_aufgaben, wa_message):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')

    content = content.replace('{current_date}', current_date)
    content = content.replace('{current_time}', current_time)
    content = content.replace('{notion_aufgaben}', str(notion_aufgaben))
    content = content.replace('{wa_message}', wa_message)

    return content


def get_prompt(notion_aufgaben, wa_message):
    return replace_placeholders("app/utils/prompts/prompt_raw.txt", notion_aufgaben, wa_message)
