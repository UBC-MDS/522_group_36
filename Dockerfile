FROM --platform=linux/amd64 quay.io/jupyter/minimal-notebook:afe30f0c9ad8

COPY conda-linux-64.lock /tmp/conda-linux-64.lock
#COPY conda-osx-arm64.lock /tmp/conda-osx-arm64.lock

USER root

# install lmodern for Quarto PDF rendering
# RUN sudo apt update \
#     && sudo apt install -y lmodern

# USER $NB_UID

RUN conda update --quiet --file /tmp/conda-linux-64.lock \
    && conda clean --all -y -f \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

RUN pip install deepchecks==0.18.1