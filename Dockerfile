# Använd den officiella Jenkins Docker-bilden
FROM jenkins/jenkins:2.462.3-jdk17

# Kör som root för att installera Docker CLI i Jenkins-bilden
USER root

# Uppdatera paket och installera Docker CLI
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli

# Byt tillbaka till Jenkins-användaren
USER jenkins

# Installera Jenkins-plugins för att hantera Docker
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"
