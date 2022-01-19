# This file defines the Docker container that will contain the weather app.
# From the source image #python
FROM python:3.6-slim
# Identify maintainer
LABEL maintainer = "niry.hoareau@gmail.com"
# Set the default working directory
WORKDIR /app/
COPY weather.py requirements.txt city.list.json /app/
RUN pip install -r requirements.txt
CMD ["python","./weather.py"]
# When the container starts, run this
ENTRYPOINT python ./weather.py
