# CampStories

CampStories is a full-stack application built with Django and Flutter. It provides users with a platform to create, share, and enjoy stories. The application incorporates several technologies to deliver a smooth and interactive user experience.

## Technologies Used


### Backend (Django)

- Django: A high-level Python web framework that provides a robust foundation for building web applications.
- Django REST Framework: A powerful toolkit for building Web APIs using Django, enabling easy API development and integration.
- Django Signals: A mechanism in Django for sending and receiving signals, which allows decoupled applications to get notified when certain actions occur.
- Boto3: The AWS SDK for Python, used to interact with Amazon Polly for text-to-speech conversion and generating audio files.
- Twilio: A cloud communications platform used for sending SMS messages to users.
visit requirements.txt for more info' on packages needed
### Frontend (Flutter)

- Flutter: An open-source UI software development kit created by Google for building cross-platform applications for mobile, web, and desktop.
- Dart: The programming language used by Flutter to build expressive and performant applications.
- Flutter SDK: The software development kit containing all the necessary tools and libraries for Flutter development.
- Flutter HTTP Package: A package that provides convenient methods for making HTTP requests and interacting with APIs.

## Functionality and Workflow

The CampStories application follows the typical workflow of a story-sharing platform:

1. User Registration and Authentication: Users can create an account and log in to access the application's features.
2. Story Creation: Logged-in users can create new stories by providing the title, content, age range, gender, story type, and optional picture.
3. Audio Generation: When a new story is created, the application automatically generates an audio file by converting the story content into speech using Amazon Polly.
4. Picture Assignment: Additionally, a random picture matching the story's genre is assigned to the story using the StoryPictureRand model.
5. Story Sharing: Users can share their stories with others by providing a unique code associated with each story.
6. User Profiles: Users can create profiles, set their preferences (name, gender, age, profile image), and view their story scores.
7. SMS Notifications: The application utilizes Twilio to send SMS notifications to users, such as when a story is shared or a new code is generated.
8. API Endpoints: The Django REST Framework is used to create API endpoints for various operations, enabling communication between the backend and the Flutter frontend.

#Backend

## Important Note Regarding Story Generation !!!

The stories generated by the `CustomStory()` view, which utilizes the OpenAI API, may not always meet the expected quality and may not fit well within the specified time ranges and age ranges. Please note that this is primarily due to limitations or variations in the responses from the OpenAI API.

Furthermore, it is essential to highlight that the generated stories are **NOT SAFE** for all audiences. The content produced by the API may include mature themes or language, which may not be suitable for users of all ages or in all contexts.

To improve the overall quality of the stories and ensure a better fit with the specified time ranges and age ranges, it is recommended to manually populate the database using the Django admin panel. The admin panel allows you to enter and customize stories with more control over their content and suitability for different age ranges.

It's worth mentioning that when using the prompts provided in the `generate_story()` function directly in the OpenAI GPT interface, the generated stories tend to be of **far better quality**. Therefore, manually adding such high-quality stories to the database will significantly enhance the overall experience and content of the application.

Please exercise caution and review the stories generated by the API to ensure they meet your standards and align with the intended audience before using them within the application.

## Guide


This guide provides an overview of the application's backend structure and functionality. Each file in the project contains detailed comments documenting the steps and functionality. Below is a summary of the key files and their purpose:

- **Amazon Polly API**: The application uses the Amazon Polly API to generate audio for stories. To use this feature, you need to set up an AWS account, configure the necessary credentials, and ensure that you have the required permissions to access the Polly API.

- **OpenAI API**: The application leverages the OpenAI API for custom story generation. To use this functionality, you need to create an OpenAI account, obtain an API key, and ensure that you have an active subscription to the OpenAI service.

- **Twilio**: The application utilizes the Twilio API for sending SMS messages. To enable this feature, you need to sign up for a Twilio account, obtain the necessary credentials, and configure the integration with your Twilio account.

Please consult the relevant documentation and official websites of these services for detailed instructions on setting up and configuring each one. It's important to note that additional costs may be associated with using these services, depending on your usage and subscription plans.

**models.py**: This file defines the database models used in the application. Each model represents a table in the database and includes fields for storing data related to users, codes, profiles, and stories. The comments within the file explain the purpose of each field and provide additional information where necessary.

**signals.py**: This file contains the signal handlers for the application. Signals are used to perform certain actions when specific events occur, such as creating a code for a user or generating audio and picture for a story. The comments within the file explain the purpose and implementation of each signal handler.

**utils.py**: This file includes utility functions used throughout the application. These functions handle tasks such as generating audio for a story using the Amazon Polly service, generating a random picture for a story, and sending SMS messages using the Twilio API. The comments within the file provide detailed explanations of each function's purpose and usage.

**views.py**: This file defines the views for the application's API endpoints. Each view corresponds to a specific URL and handles incoming requests, processes data, and returns responses. The comments within the file document the functionality of each view and explain any additional considerations.

Additional files: The project may include other files such as `settings.py`, `urls.py`, and `serializers.py` that are essential for configuring the Django project, defining URL patterns, and serializing data for API responses. Each of these files is thoroughly commented to explain their role and functionality.


### File Structure

The project's file structure is organized as follows:

- `campstories/`: The project's root directory containing the Django settings and configuration files.
- `api/`: The Django app directory containing the models, views, serializers, and API-related files.
- `flutter_app/`: The Flutter app directory containing the Dart code for the mobile application.
- `media/`: The directory for storing media files, such as story pictures and audio files.

#Please refer to the comments within each file for more detailed information on their implementation and how they contribute to the overall functionality of the application.


