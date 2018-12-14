FROM python:3
RUN touch /var/log/access.log && ln -s /var/log/access.log /tmp/access.log
ADD httpmonitor /usr/local/bin
ENTRYPOINT ["/usr/local/bin/httpmonitor"]
