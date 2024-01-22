FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

# OpenCV Version
ARG OPENCV_VERSION="4.8.0"

# Install build dependencies
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
        build-essential binutils \
        ca-certificates cmake cmake-qt-gui curl \
        dbus-x11 \
        ffmpeg \
        gdb gcc g++ gfortran git \
        tar \
        lsb-release \
        procps \
        manpages-dev \
        unzip \
        zip \
        wget \
        xauth \
        swig \
        python3-pip python3-dev python3-numpy python3-distutils \
        python3-setuptools python3-pyqt5 python3-opencv \
        libboost-python-dev libboost-thread-dev libatlas-base-dev libavcodec-dev \
        libavformat-dev libavutil-dev libcanberra-gtk3-module libeigen3-dev \
        libglew-dev libgl1-mesa-dev libgl1-mesa-glx libglib2.0-0 libgtk2.0-dev \
        libgtk-3-dev libjpeg-dev libjpeg8-dev libjpeg-turbo8-dev liblapack-dev \
        liblapacke-dev libopenblas-dev libopencv-dev libpng-dev libpostproc-dev \
        libpq-dev libsm6 libswscale-dev libtbb-dev libtbb2 libtesseract-dev \
        libtiff-dev libtiff5-dev libv4l-dev libx11-dev libxext6 libxine2-dev \
        libxrender-dev libxvidcore-dev libx264-dev libgtkglext1 libgtkglext1-dev \
        libvtk9-dev libdc1394-dev libgstreamer-plugins-base1.0-dev \
        libgstreamer1.0-dev libopenexr-dev \
        openexr \
        pkg-config \
        qv4l2 \
        v4l-utils \
        zlib1g-dev \
        locales \
        && locale-gen en_US.UTF-8 \
        && LC_ALL=en_US.UTF-8 \
        && rm -rf /var/lib/apt/lists/* \
        && apt-get clean

WORKDIR /opencv
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
    && wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.zip \
    && unzip opencv.zip \
    && unzip opencv_contrib.zip \
    && mv opencv-${OPENCV_VERSION} opencv \
    && mv opencv_contrib-${OPENCV_VERSION} opencv_contrib

RUN mkdir /opencv/opencv/build
WORKDIR /opencv/opencv/build

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
 -D CMAKE_INSTALL_PREFIX=/usr/local \
 -D INSTALL_PYTHON_EXAMPLES=ON \
 -D INSTALL_C_EXAMPLES=ON \
 -D OPENCV_ENABLE_NONFREE=ON \
 -D OPENCV_GENERATE_PKGCONFIG=ON \
 -D OPENCV_EXTRA_MODULES_PATH=/opencv/opencv_contrib/modules \
 -D PYTHON_EXECUTABLE=/usr/local/bin/python \
 -D WITH_CUDA=ON \
 -D BUILD_EXAMPLES=ON .. \
    && make -j$(nproc) && make install && ldconfig

WORKDIR /usr/app

ENV PIP_DEFAULT_TIMEOUT=500

USER root
ARG DEBIAN_FRONTEND=noninteractive

RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections && \
    apt-get update && \
    apt install wget ffmpeg libsndfile1 build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev -y
RUN apt-get install -y git
RUN apt install python3-pip -y
RUN apt-get install git-lfs
RUN git clone https://huggingface.co/datasets/nuwandaa/facedata
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib/python3.8/dist-packages/nvidia/cudnn/lib"

COPY requirements.txt /usr/app/requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--workers", "3"]
