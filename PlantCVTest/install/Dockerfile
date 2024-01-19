FROM jupyter/minimal-notebook
LABEL maintainer="PlantCV <plantcv@danforthcenter.org>"

USER root

RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Copy source files
COPY plant_environment.yml /tmp/plant_environment.yml

# Change working directory and modify requirements.txt
#RUN cd /tmp && sed -i'' -e 's/opencv.*//g' requirements.txt

# Install PlantCV
RUN mamba env create -f plant_environment.yml && conda clean --all -fy
#RUN cd /tmp && mamba install --quiet --yes -c conda-forge --file requirements.txt 'opencv' && conda clean --all -f -y

# Install PlantCV Python prerequisites and PlantCV
RUN cd /tmp && python setup.py install

USER $NB_UID
