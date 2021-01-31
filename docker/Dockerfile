FROM alpine:latest
# FROM alpine:3.8 # Fixes non-zero return (139) during the next RUN command
# Reference: https://stackoverflow.com/questions/54651121/alpine-docker-returned-a-non-zero-code-139

RUN apk add --update redis supervisor python-dev \
    py-pip \
    build-base \
    python3 \
    tzdata \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/* 

# Do timezone stuff
ARG TZ=America/Denver
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && \
  echo $TZ > /etc/timezone && \
  apk del tzdata

COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

RUN mkdir -p /usr/local/bin/app/dashboards
COPY src/ /usr/local/bin/app/
RUN mkdir -p /tmp/dashboards/


COPY docker/supervisord.conf /etc/supervisor/supervisord.conf
USER root
RUN mkdir /root/logs
RUN sh -c "cd /root && virtualenv tb-env && source /root/tb-env/bin/activate && pip install tipboard"

# Handle tipboard-specific config (this is gross, so let's change it later)
COPY dashboards/layout_config.yaml /root/.tipboard/
COPY dashboards/settings-local.py /root/.tipboard/

EXPOSE 7272
CMD ["/usr/bin/supervisord", "-j", "/root/supervisord.pid", "-c", "/etc/supervisor/supervisord.conf"]
