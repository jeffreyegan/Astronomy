FROM nvidia/cuda:11.4.0-devel-ubuntu20.04
LABEL description="spaceawareness"
LABEL version="0.1.0"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-wheel \
    python3-setuptools \
    libgeos-dev \
    git && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN pip3 install --no-cache-dir -U install setuptools pip
RUN pip3 install --no-cache-dir "cupy-cuda114" \
    numba numpy pandas pickle5 matplotlib seaborn jplephem skyfield skyfield-data poliastro cartopy geopy

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

#RUN pip uninstall shapely
#RUN pip install --no-binary :all: shapely

WORKDIR /code
#CMD ["python", "main.py"]