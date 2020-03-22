FROM alpine:latest

RUN apk add --update redis supervisor python-dev \
    py-pip \
    build-base \
    python3 \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/* 

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
