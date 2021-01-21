import rospy
from chatbot.srv import Message, MessageResponse
from chatbot.chat_assistant import Assistant


class Server():
    assistant = None
    service = None

    def __init__(self):
        print("chat_server.py", "__init__")

        # initialize node
        rospy.init_node('chat_server')

        # register service
        self.service = rospy.Service(
            'chat_server', Message, self.handle_message)

        # initialize watson
        self.assistant = Assistant()

    def start(self):
        print("chat_server.py", "start")

        # start node
        print("Ready to tell some jokes, random facts, or what ever!")
        rospy.spin()

        # close assistant session when node is stopped
        self.assistant.close()

    def handle_message(self, request):
        print("chat_server.py", "handle_message", request)

        # fetch and return answer from watson
        answer = self.assistant.message(request.message)
        return MessageResponse(answer)


def main():
    server = Server()
    server.start()
