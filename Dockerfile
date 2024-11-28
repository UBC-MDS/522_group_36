FROM --platform=linux/amd64 quay.io/jupyter/minimal-notebook:afe30f0c9ad8

COPY conda-linux-64.lock /tmp/conda-linux-64.lock

# Initialize conda and use conda instead of mamba
RUN conda init bash && \
    . /opt/conda/etc/profile.d/conda.sh && \
    conda activate base && \
    conda install --quiet --file /tmp/conda-linux-64.lock && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"