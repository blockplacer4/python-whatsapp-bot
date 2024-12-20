from openai import OpenAI
import shelve
from dotenv import load_dotenv
from app.utils.prompts import prompt, reminder_prompt
from app.utils import notion_utils, reminder_utils
import os
import time
import logging
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=OPENAI_API_KEY)


# Use context manager to ensure the shelf file is closed properly
def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)


def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id


def run_assistant(thread, name):
    assistant = client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    retry_count = 0
    max_retries = 5

    while run.status != "completed":
        if retry_count >= max_retries:
            logging.error("Maximum retries reached. Ending run.")
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="assistant",
                content="Sorry Cheff, mein Backend funktioniert gerade nicht."
            )
            break

        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action":
            tool_outputs = []

            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                function_name = tool_call.function.name
                function_arguments = json.loads(tool_call.function.arguments)

                try:
                    result = reminder_utils.execute_function(function_name, **function_arguments)
                    if not isinstance(result, str):
                        result = json.dumps(result)
                except ValueError as e:
                    logging.warning(str(e))
                    result = json.dumps({"error": str(e)})

                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": result
                })

            if tool_outputs:
                try:
                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    logging.info("Tool outputs submitted successfully.")
                except Exception as e:
                    logging.error(f"Failed to submit tool outputs: {e}")
                    retry_count += 1
            else:
                logging.info("No tool outputs to submit.")

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value if messages.data else ""
    logging.info(f"Generated message: {new_message}")
    return new_message


def generate_response(message_body, wa_id, name, which_prompt='userprompt'):
    thread_id = check_if_thread_exists(wa_id)

    if thread_id is None:
        logging.info(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)
        thread_id = thread.id
    else:
        logging.info(f"Retrieving existing thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.retrieve(thread_id)

    notion_data = notion_utils.get_all_pages("13586c44936d80078ae6eae78d36f53d")
    # make a list with "which prompt" and then get it from this yk | Hier Zukunft Janosch, zu Aufwendig
    content_prompt = prompt.get_prompt(notion_data, message_body) if which_prompt == 'userprompt' else reminder_prompt.get_prompt(message_body)

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content_prompt,
    )

    new_message = run_assistant(thread, name)

    return new_message
