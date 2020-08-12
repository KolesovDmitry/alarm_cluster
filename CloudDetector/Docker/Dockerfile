FROM debian:9

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update
RUN apt-get install --no-install-recommends -y \
    python-gdal grass grass-dev \
    python-pip

RUN pip install grass-session


RUN mkdir -p /opt/DATA
RUN mkdir -p /opt/GRASSDATA
RUN mkdir -p /opt/raster_processor

RUN grass -c EPSG:4326 /opt/GRASSDATA/LatLon

# COPY raster_processor/* /opt/raster_processor




