import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "PATH TO YOUR SERVICE ACCOUNT JSON KEY"
# don't forget to get your service account JSON key from google cloud platform

import dialogflow_v2 as dialogflow
dialogflow_sessions_client = dialogflow.SessionsClient()
PROJECT_ID = "YOUR DIALOGFLOW PROJECT ID"


def detect_intent_from_text(text, session_id, language_code='en'):
	session = dialogflow_sessions_client.session_path(PROJECT_ID, session_id)
	text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
	query_input = dialogflow.types.QueryInput(text=text_input)
	response = dialogflow_sessions_client.detect_intent(session=session, query_input=query_input)
	return response.query_result



def get_reply(query, chat_id):
	response = detect_intent_from_text(query, chat_id)
	print("-----------------------------------------------")
	print(response)

	if response.intent.display_name == 'NewsIntent':
		print(dict(response.parameters))
		return "NewsIntent", dict(response.parameters)
	else:
		return "small_talk", response.fulfillment_text
