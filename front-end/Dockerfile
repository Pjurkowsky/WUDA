FROM python:3.12-alpine


RUN adduser docent -h /home/docent -D
USER docent

WORKDIR /home/docent/app

COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt

RUN mkdir static templates utils
COPY ./static ./static
COPY ./templates ./templates
COPY ./utils ./utils

COPY ./app.py ./settings.py ./test_app.py .

EXPOSE 8000


CMD [ "python3" , "app.py" ]

