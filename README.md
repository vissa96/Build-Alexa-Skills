# Build-Alexa-Skills for Alexa to talk about Azure resources in your connected subscription

This repo talks about building a custom Alexa skill which is integrated with cloud tools. I have created this overview to walk those new to voice development through the process of making an Alexa skill.

# Steps

1) The skill interface is implemented within the Amazon Alexa developers platform. This means that you’ll need an Amazon Developers Services (ADS) account in order to build the skill and its interaction model.

2) Sign in to your ADS account and choose Alexa.

3) Click the “Alexa Skills Kit”

4) Click the “Start a Skill” button.

5) Click the “Create Skill” button (this will open the “Create a new skill” form).

6) Enter your skill name in the “Skill name field”, and select “Custom”.

# Part 1: Building the Intents via developer portal

1) Select the “Invocation” tab.

2) Enter invoke name in the “Skill Invocation Name” field.

3) Set up required intents. Each intent will perform a specific function. Intent A can be integrated with azure to read all listed VM's.
Intent B can talk to service now to read all P1 tickets.

4) Select the "Utterance tabs"

5) Enter the utterance text in the “Sample Utterances” filed in the form of “tell me about {}”.

# Part 2: Choosing the Endpoints

1) Click the “Endpoints” tab.

2) Select the “AWS Lambda function”.

# Part 3: Creating the AWS Lambda Function

There are three main request types:

LaunchRequest is sent within the event to the Lambda function when the user invokes the skill by saying its invocation name.

IntentRequest is sent within the event to the Lambda function when the user interacts with the skill, i.e. when his speech request is mapped to an intent. The intent is also inscribed in the event.

SessionEndedRequest is sent within the event to the Lambda function when the session ends, due to an error, when the user says “exit”, when the user doesn’t respond while the device is listening, or when the user says something that doesn’t match an intent defined in your skill interface while the device is listening.

1) Log in to your account and choose the Lambda services.

2) In the upper right corner select “N. Virginia”, to make the Alexa Skill Kit trigger available to the AWS Lambda function.

3) Click the “Create a function” button.

4) In the “Create function” form select “Author from scratch”

5) From the “Runtime” list select Python 3.6.

6) Select the “Alexa Skills Kit” in the “Add triggers” list.

7) Copy paste the code given. Be sure to have existing Beam and Azure subscribtions.

# Important

This is not my full implementation for Alexa skills, but a part of code for what I built. I extended this to connect with muiltiple platforms and gather information to enhance customer experience. Please get in touch through email for further information.


