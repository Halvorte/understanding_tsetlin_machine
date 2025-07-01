#FROM ubuntu:20.04
FROM ubuntu:24.04

# Set environment variables for non-interactive apt-get installs
ENV DEBIAN_FRONTEND=noninteractive

# Update apt, install Python 3, pip, and other necessary build tools
# Python 3.8 is the default for Ubuntu 20.04
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    neofetch && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user (best practice)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    apt-get update && \
    apt-get install -y sudo && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#WORKDIR /
# Sets working directory to /app. If not exist, will create. COPY RUN CMD will execute to /app
WORKDIR /app

# Change ownership of /app to the new user
RUN chown $USERNAME:$USERNAME /app

# Switch to the non-root user
USER $USERNAME

# Copy only requirements.txt first to leverage Docker's build cache
COPY requirements.txt ./
# COPY all files from project to container 
#COPY . .

# ADD

# Install Python dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN apt-get update && apt-get install neofetch && pip install --no-cache-dir && -r requirements

# Copy the rest of your application code
COPY . .

# ENV


# Define the default command to run when the container starts
CMD ["python3", "main.py"] # Ensure you use python3 as the command