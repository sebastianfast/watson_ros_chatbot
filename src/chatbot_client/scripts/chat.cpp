#include "ros/ros.h"
#include "chatbot/Message.h"
#include <sstream>
#include <cstdlib>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "chat");

  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<chatbot::Message>("chat_server");

  chatbot::Message srv;

  while (ros::ok())
  {
    std::cout << "You: ";
    std::getline(std::cin, srv.request.message);

    if (client.call(srv))
    {
      std::cout << "Bot: " << srv.response.answer << std::endl;
    }
    else
    {
      ROS_ERROR("Failed to call service chat_server");
      return 1;
    }

    ros::spinOnce();
  }

  return 0;
}