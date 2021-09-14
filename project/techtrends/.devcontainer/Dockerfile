FROM ubuntu:20.04

# Configure to reduce warnings and limitations as instruction from official VSCode Remote-Containers.
# See https://code.visualstudio.com/docs/remote/containers-advanced#_reducing-dockerfile-build-warnings.
ENV DEBIAN_FRONTEND=noninteractive

# Setup python
RUN apt-get -y update \
  && apt-get -y install python3 python3-pip python3-venv \
  && update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Verify git, process tools, lsb-release (common in install instructions for CLIs) installed.
RUN apt-get -y install git iproute2 procps lsb-release vim build-essential python3

# Add python application.
WORKDIR /opt/src/app/python-helloworld/
COPY . .
RUN pip install -r requirements.txt

# Add sqlite3 (for troubleshooting purpose)
RUN apt-get -y install sqlite3

# Cleanup
RUN apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# Revert workaround at top layer.
ENV DEBIAN_FRONTEND=dialog

# Expose service ports (3111: the website's default port).
EXPOSE 3111

