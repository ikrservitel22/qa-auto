FROM python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    git \
    nano \
    vim \
    curl \
    wget

RUN useradd -ms /bin/bash developer

RUN echo "developer:developer" | chpasswd

RUN adduser developer sudo

RUN echo "developer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir /var/run/sshd

RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

WORKDIR /workspace

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chown -R developer:developer /workspace

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]