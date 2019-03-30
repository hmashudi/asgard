FROM ubuntu:16.04

RUN apt-get update && apt-get install -y openssh-server python3-pip
RUN mkdir /var/run/sshd
RUN echo 'root:PASSWORD' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN pip3 install tailer
ADD alphaclient.py /
COPY startup.sh /

EXPOSE 22
CMD ["/bin/sh", "./startup.sh"]
