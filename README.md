# What is this?
A simple chatbot using IBM Watson Assistant, IBM Cloud Functions and ROS Noetic as well as Docker and VSCode for containerized development.

The chatbot replies with chuck norris jokes and cat facts on demand.

# Usage
Build this project in your ros favourite environment. I used [devrt/ros-devcontainer-vscode](https://github.com/devrt/ros-devcontainer-vscode) to create a ros devcontainer within VSCode, with adjusted settings.

## Creating the Watson Assistant
I will not go into detail of how to setup the assistant. I followed [this tutorial](https://cloud.ibm.com/docs/assistant?topic=assistant-dialog-webhooks) and got caught up with a few things that weren't mentioned in there. You will find those things in the following.

### Webhook Setup
The webhook setup was where I experienced problems diverging from the instructions of the tutorial mentioned abve.

1. The webhook URL must append the parameter `?blocking=true`, i.e. `https://eu-gb.functions.cloud.ibm.com/api/v1/namespaces/<your namespace>/actions/joke?blocking=true`
2. You must set a basic authorization header. Your webhook API key contains the username before the colon and the password after the colon
3. You must set a header with `Content-Type=application/json`

### Dialog Nodes
The only thing different to the above mentioned tutorial is the returned object from the webhook. The object has a different parameter structure and thus you cannot access a joke's or fact's response by `$webhook_result_1.response.fact` or `$webhook_result_2.response.joke`.

1. For facts you have to use `$webhook_result_1.response.result.response.fact`
2. For jokes you have to use `$webhook_result_2.response.result.response.value.joke`

### Getting the credentials
For the steps you will need to fetch the assistant's ID, API key, and access url. You can find the API key and access url by navigating to your Watson assistant instance, in my case it is named `Watson Assistant-8w`. The assistant ID is found by then clicking on `Launch Watson Assistant` and navigating the the settings of your just created assistant.

The credentials look like this:

    API key: xexP-<more characters>
    URL: https://api.eu-de.assistant.watson.cloud.ibm.com/instances/<instance id>
    Assistant ID: e099ecb3-5651-<more characters>

## Setting up the devcontainer

Follow [the instructions here](https://github.com/devrt/ros-devcontainer-vscode) and then apply the following modifications.

### Passing environmental variables

We need to pass the variables `ASSISTANT_APIKEY`, `ASSISTANT_URL`, and `ASSISTANT_ID` that hold the necessary information to connect to the watson assistant. These variables are passed within an `.env`-file located in the root of the cloned devcontainer.

Pass the values in `ros-devcontainer-vscode/.env`:

    ASSISTANT_APIKEY=<assistant_apikey>
    ASSISTANT_URL=<assistant_url>
    ASSISTANT_ID=<assistant_id>

Uncomment the following lines in `ros-devcontainer-vscode/docker-compose.yml` :

    workspace:
      env_file:
        - .env

Now, the environmental variables in `.env` will be passed to the container on launch.

### Installing IBM Watson Python package

Create a Dockerfile `ros-devcontainer-vscode/Dockerfile`. You may choose another name or rename the already existent Dockerfile. Within the Dockerfile, paste following code, which will install the IBM Watson python package:

    FROM devrt/ros-devcontainer-vscode:noetic-desktop

    # Install IBM Watson
    RUN pip install --upgrade --user \
        ibm-watson

Change your `ros-devcontainer-vscode/docker-compose.yml` into the following:

    workspace:
      build:
        context: .
        dockerfile: Dockerfile
      #image: devrt/ros-devcontainer-vscode:noetic-desktop

### Launching the chat and chatbot

You should now be ready to launch the chat client and server. Connect to your ros environment and start `roscore`.

## Pull this repo
Pull this repo in your ros environment.

## Start the chatbot server
In a new terminal, source the project and run the server:

    source devel/setup.sh
    rosrun chatbot server

The server should by now have printed

> Ready to tell some jokes, random facts, or what ever!

## Start the chatbot client
In a new terminal, source the project and run the client:

    source devel/setup.sh
    rosrun chatbot_client chat

You should now see a console output indicating that you can type in your message. Type in "joke" for a chuck norris joke and "fact" for a cat fact and press enter.

> You: joke\
> Bot: Chuck Norris is the only person who can simultaneously hold and fire FIVE Uzis: One in each hand, one in each foot -- and the 5th one he roundhouse-kicks into the air, so that it sprays bullets.\
>
> You: fact\
> Bot: In an average year, cat owners in the United States spend over $2 billion on cat food.