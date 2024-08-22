FROM nikolaik/python-nodejs:python3.12-nodejs22

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create the cineuser user and group
RUN useradd -ms /bin/bash cineuser

# Set working directory and copy files with correct ownership
WORKDIR /app/
COPY --chown=cineuser:cineuser . /app/

# Adjust permissions
RUN chmod -R 755 /app/

# Copy .env file
COPY .env /app/.env

# Upgrade pip and install dependencies
RUN python -m pip install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir --requirement requirements.txt

# Use JSON syntax for CMD
CMD python3 -m CineWinx
