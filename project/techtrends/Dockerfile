FROM python:2.7 

# Configure to reduce warnings and limitations as instruction from official VSCode Remote-Containers.
# See https://code.visualstudio.com/docs/remote/containers-advanced#_reducing-dockerfile-build-warnings.
ENV DEBIAN_FRONTEND=noninteractive

# Setup python
RUN apt-get -y update

# Verify git, process tools, lsb-release (common in install instructions for CLIs) installed.
RUN apt-get -y install git iproute2 procps lsb-release vim build-essential

# Add sqlite3 (for troubleshooting purpose)
RUN apt-get -y install sqlite3

# Add python application and install dependencies.
WORKDIR /opt/src/app/techtrends/
COPY . .
RUN pip install -r requirements.txt

# Init the database
RUN python init_db.py

# Cleanup
RUN apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# Revert workaround at top layer.
ENV DEBIAN_FRONTEND=dialog

# Expose service ports (3111: the website's default port).
EXPOSE 3111

# Run the application
CMD [ "python", "app.py" ]
