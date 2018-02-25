FROM python:3.6-alpine
ARG workdir=/sparkabowl

WORKDIR $workdir
COPY . $workdir

# Will always be test-requirements.txt
RUN pip install -r test-requirements.txt

