#!/bin/bash


ip=$1
droplet=$2


echo ip droplet $ip
echo name droplet $droplet;


#ssh root@$ip "\
#  adduser dockermachine && \
#  usermod -aG sudo dockermachine && \
#  echo dockermachine ALL=NOPASSWD: ALL &>> /etc/sudoers && \
#  cp -R /root/.ssh /home/dockermachine/ && \
#  chmod -R 755 /home/dockermachine/.ssh && \
#  chown -R dockermachine:dockermachine /home/dockermachine/.ssh
#"


echo create machine


#docker-machine create --driver generic --generic-ip-address=$ip --generic-ssh-key /home/evgeniy/.ssh/id_rsa --generic-ssh-user dockermachine $droplet
#docker-machine env $droplet
#eval $(docker-machine env $droplet)


docker-machine ssh $droplet "\
  sudo usermod -aG docker dockermachine && \
  sudo chmod 777 /var/run/docker.sock && \
  sudo apt update && \
  sudo apt upgrade -y && \
  sudo apt dist-upgrade -y && \
  sudo apt install python3-pip -y && \
  sudo pip3 install docker-compose && \
  docker-compose -v
"
