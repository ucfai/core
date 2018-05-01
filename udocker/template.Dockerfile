FROM %%base%%

RUN apt-get update

## OpenCV & Conda Dependencies
RUN apt-get install -y  \
build-essential  bzip2          cmake             libavcodec-dev   \
libavformat-dev  libavutil-dev  libdc1394-22-dev  libgl1-mesa-dev  \
libgtk2.0-dev    libjasper-dev  libjpeg-dev       libpng-dev       \
libswscale-dev   libtbb-dev     libtiff-dev       libv4l-dev       \
libxext6         pkg-config     unzip             wget                 

## Conda
RUN    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-%%conda%%-Linux-x86_64.sh \
    && /bin/bash Miniconda3-%%conda%%-Linux-x86_64.sh -b -p /opt/conda \
    && rm Miniconda3-%%conda%%-Linux-x86_64.sh
ENV PATH /opt/conda/bin:$PATH

ADD env/%%type%%.yml /%%type%%.yml
RUN conda env create -f /%%type%%.yml

ENV PATH /opt/conda/envs/%%name%%/bin:$PATH

## Cleaning up
RUN apt-get clean  \
&& rm -rf /var/lib/apt/lists/*  \
&& conda clean --tarballs -y  \
&& conda clean --packages -y

WORKDIR "/notebooks"
EXPOSE 8888

CMD ["jupyter", "notebook", \
	 "--ip=0.0.0.0", "--allow-root", \
	 "--NotebookApp.token=''", "--no-browser"]