import os
from ibm_watson import AssistantV2


class Assistant():
    ASSISTANT_ID = None
    SESSION_ID = None

    assistant = None

    def __init__(self):
        print("watson.py", "__init__")

        # fetch env variables
        self.ASSISTANT_ID = os.environ['ASSISTANT_ID']
        self.ASSISTANT_URL = os.environ['ASSISTANT_URL']

        # Initialize assistant
        self.assistant = AssistantV2(version='2020-04-01')
        self.assistant.set_service_url(self.ASSISTANT_URL)

        # Create session to work with
        self.SESSION_ID = self.assistant.create_session(
            self.ASSISTANT_ID).get_result()['session_id']

    def close(self):
        print("watson.py", "close")

        # delete session
        self.assistant.delete_session(
            self.ASSISTANT_ID, self.SESSION_ID).get_result()

    def message(self, text):
        print("watson.py", "message", text)

        # send text to assistant
        response = self.assistant.message(
            self.ASSISTANT_ID,
            self.SESSION_ID,
            input={'text': text},
            context={
                'metadata': {
                    'deployment': 'myDeployment'
                }
            }).get_result()

        # extract and return answer
        return response["output"]["generic"][0]["text"]


if __name__ == '__main__':
    assistant = Assistant()
    assistant.message("joke")
    assistant.close()
