# Flask-swiftdoc-1.0
Flask app

##Before running:
1. Check if there is a debug_environment.cfg file present in the flask-swiftdoc directory
2. Create a file debug_environment.cfg in the same folder as app.py.
3. Include in the file:

                        ENV="development"
                        SECRET_KEY="(any key)"
                        DEBUG = True
                        TESTING = True

##Command Line Usage:

Run the following command from the flask-swiftdoc directory to start the application on the local host:

      python3 app.py



##Dockerised Usage:

Run the following command in the same directory as the app.py file to build the container and start the application consequently with docker desktop running in the background:


      docker compose up
Please note that if you want to run in docker desktop then:

      CMD ["app.py" ] //Please put in Dockerfile
      #CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app //Please comment using # or delete in Dockerfile

& if you want to run in google cloud run then:

      #CMD ["app.py" ] //Please comment using # or delete in Dockerfile
      CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app //Please put in Dockerfile

##Google Cloud Usage:
First, we have to install google cloud sdk in operating system(mac,linux,windows).
Secondly, we have to run the following command in the same directory as the app.py file to build the container and start the application:


      gcloud run deploy
Please note that if you want to run in docker desktop then:

      CMD ["app.py" ] //Please put in Dockerfile
      #CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app //Please comment using # or delete in Dockerfile

& if you want to run in google cloud run then:

      #CMD ["app.py" ] //Please comment using # or delete in Dockerfile
      CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app //Please put in Dockerfile
##Generating Report:

1. Upload the required files in the corresponding steps.
2. Click generate and hold on for 15 seconds before downloading the report.
