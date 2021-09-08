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

# Setup python web framework: Flask
RUN pip install Flask

# Setup golang
RUN apt-get -y install golang

# Cleanup
RUN apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# Revert workaround at top layer.
ENV DEBIAN_FRONTEND=dialog

# Expose service ports (5000:Flask default port, 6111:golang default port).
EXPOSE 8000
EXPOSE 5000
EXPOSE 6111

# Set working directory 
#WORKDIR /mnt/devroot/src/

