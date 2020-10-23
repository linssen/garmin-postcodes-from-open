FROM python:3.6

RUN apt-get update
RUN apt-get install -y gpsbabel

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./get_postcodes.py" ]
