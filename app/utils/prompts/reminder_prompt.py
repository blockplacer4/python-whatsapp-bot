from datetime import datetime

def replace_placeholders(file_path, reminder_data):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')

    content = content.replace('{current_date}', current_date)
    content = content.replace('{current_time}', current_time)
    content = content.replace('{reminder_data}', str(reminder_data))

    return content


def get_prompt(reminder_data):
    return replace_placeholders("app/utils/prompts/reminder_prompt_raw.txt", reminder_data)
