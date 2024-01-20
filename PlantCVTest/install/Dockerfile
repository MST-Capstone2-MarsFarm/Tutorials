#takes about 6 minutes to setup
FROM mambaorg/micromamba:1.5.6

USER root

#this is all I need for now
#If we need more packages, then we'll just keep on adding more here
RUN apt-get update && apt-get install -y libgl1-mesa-glx libfreetype6-dev libpng-dev && rm -rf /var/lib/apt/lists/*

# Copy source files
COPY --chown=$MAMBA_USER:$MAMBA_USER plant_environment.yml /tmp/plant_environment.yml

# Install PlantCV
#Mamba is orders of magnitude faster
#basically, use this image as an 'environment', and then run your code
RUN micromamba install -y -n base -f /tmp/plant_environment.yml
RUN micromamba clean --all -fy