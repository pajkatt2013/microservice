# Microservice

## Part 1: Workflow(from user perspective)

> The overall conversion flow is as follows:

![architecture](./resources/pics/architecture.png)

1. **User upload**: when a user uploads a video to be converted to MP3, that request will first hit our gateway. Our gateway will then store the video in mongodb and then put a message on our rabbitmq queue. Downstream services know that there is video to be processed in Mongodb.
2. **Converting**: The video to MP3 converter service will consume messages from the queue. It will then get the id of the video from the message, pull the video from mongodb, convert the video to MP3, then store the MP3 on mongodb. then put a new message on the queue to be consumed by the notification service that says that the conversion job is done.
3. **Notification**: The notification service consumes those messages from the queue and sends an e-mail notification to the client informing the client that the MP3 for the video that he or she uploaded is ready for download.
4. **Downloading**: The client Then uses a unique ID acquired from the notification plus his or her JWT to make requests to the API gateway to download MP3. And the API gateway will pull the MP3 from mongodb and serve it to the client.

## Part 2: Services(from system design perspective)

> There are 5 micro-services in this architecture: auth service, gateway, converter, rabbitmq, and notification.

1. **Auth**: Handles user authentication and generates JWT tokens for secure API access.
2. **Gateway**: Acts as the entry point for all client requests, routing them to appropriate services and managing data storage/retrieval in MongoDB.
3. **Converter**: Processes video-to-MP3 conversion by retrieving videos from MongoDB, performing the conversion, and storing the resulting MP3s back in MongoDB.
4. **RabbitMQ**: Manages message queuing to coordinate workflows between services like conversion and notification.
5. **Notification**: Sends email notifications to clients when the MP3 conversion is complete and ready for download.

## Part 3: Steps to deploy(on local computer)

> If you're not interested in local deployment, skip this part.

1. Pre-intallations:
   Install these tools in your local computer, you can easily intall them by googling:
   1. Docker
   2. kubectl
   3. minikube
   4. mysql
   5. python(see requirements.txt)
   6. k9s
2. Clone this github repo to your local environment
3. We will deploy this on teminal(mine is powershell):
   1. Activate python virtual environment:
      ```ps
      myvenv/Scripts/activate
      ```
   2. start mysql service(window 10):
      ```ps
      net start MySQL80
      ```
   3. Initiate mysql database(creating auth database and user table), this mysql database is for authentication purposes:
      ```ps
      Get-Content python/src/auth/init.sql | mysql -uroot -p<your_password>
      ```
      You can verify it by starting a mysql session and run commands like "show databases;":
      ```ps
      mysql -uroot -p<your_password>
      ```
   4. Deploy auth service:
      Before this step, create dockerhub repositories for auth service, for example:<your_dockerhub_username>/auth,
      then build and push
      ```ps
      cd ./python/src/auth
      docker build . -t <your_dockerhub_username>/auth:latest
      docker push <your_dockerhub_username>/auth:latest
      ```
      if error happens in build step, try pull the image first:
      ```ps
      docker pull python:3.10-slim-bullseye
      ```
      if error happens in push step, try login docker first:
      ```ps
      docker login
      ```

## Part 4: Steps to deploy(on AWS)

1. Configuring github actions

   1. Add a self-hosted runner and run it. The specific steps differ depending on the os on your local machine, mine window 10,x64. After you added and run, it should looks like this:

      ![runner_added_screenshot](./resources/pics/runner_added_screenshot.png)

      You can refer to github official docs [here](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners)

   2. Add a workflow yaml file to your git repository, must be in this specific path:"repo_name/.github/workflows/workflow_name.yml". The workflow yaml file configures the runner, trigger-event of the workflow, and specifics about the whole process. [This is a quick start of writing a workflow](https://docs.github.com/en/actions/writing-workflows/quickstart).

2. Automating the deployment
   1. We can automate the whole deployment process by just pushing to the repository(it can be configured in the workflow yaml file).
   2. See the status of the workflow on the terminal of the self-hosted runner or github UI(repository-Actions)
3. Testing the deployment

See the original tutorial that I referred to [here](https://youtu.be/hmkF77F9TLw?si=zbVzVs1qiEza6g4v).
