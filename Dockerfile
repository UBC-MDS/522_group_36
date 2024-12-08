FROM --platform=linux/amd64 quay.io/jupyter/minimal-notebook:afe30f0c9ad8
COPY conda-linux-64.lock /tmp/conda-linux-64.lock

# Switch to root for system-level operations
USER root

# Install lmodern and create necessary directories
RUN apt update && \
    apt install -y lmodern && \
    mkdir -p /home/jovyan/.cache/conda && \
    chown -R $NB_UID:$NB_GID /home/jovyan/.cache && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Switch to notebook user for conda operations
USER $NB_UID

# Update conda and install packages
RUN conda update --quiet --file /tmp/conda-linux-64.lock && \
    conda clean --all -y -f

# Install deepchecks
RUN pip install deepchecks==0.18.1
# RUN pip install quarto-cli==1.5.57
# RUN pip install tabulate==0.9.0

# Final user setting
USER $NB_UID