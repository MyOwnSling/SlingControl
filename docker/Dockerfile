FROM alpine:latest

# Add system packages
RUN apk add python3

# Add python packages (after updating pip)
COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Add app content
RUN mkdir -p /usr/local/bin/app
COPY src/ /usr/local/bin/app/