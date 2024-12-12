FROM --platform=linux/amd64 quay.io/jupyter/minimal-notebook:afe30f0c9ad8
COPY conda-linux-64.lock /tmp/conda-linux-64.lock

RUN conda init bash && \
    . /opt/conda/etc/profile.d/conda.sh && \
    conda activate base && \
    conda install --quiet --file /tmp/conda-linux-64.lock && \
    conda clean --all -y -f && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Switch to root for system-level operations
USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends lmodern librsvg2-bin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/jovyan/.cache/conda && \
    chown -R $NB_UID:$NB_GID /home/jovyan/.cache && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

RUN pip install \
pandera==0.21.0 \
pytest==8.3.3 \
black==24.10.0 \
vegafusion==2.0.1 \
vegafusion-python-embed==1.6.9 \
vl-convert-python==1.7.0 \
deepchecks==0.18.1 

# Switch to notebook user for conda operations
USER $NB_UID