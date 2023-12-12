FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive

# Install tools.
RUN  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list 
RUN  apt-get update
RUN  apt-get -y upgrade
RUN  apt-get install -y build-essential
RUN  apt-get install -y software-properties-common
RUN  apt-get install -y byobu curl git htop man unzip vim wget
RUN  add-apt-repository -y ppa:nginx/stable
RUN  add-apt-repository ppa:deadsnakes/ppa

# Validate python version
RUN echo python3 --version

# Install project requirements
RUN  apt-get install -yf build-essential gcc python3.10
RUN  update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN  apt-get install -yf python3.10-distutils
RUN  apt-get -y upgrade
RUN  apt-get install -yf python3-setuptools binutils libproj-dev gdal-bin postgresql-server-dev-all libjpeg8-dev
RUN  curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN  apt-get install -yf python3-dev

# Install supervisor
RUN apt-get install -y supervisor
RUN mkdir -p /etc/supervisor/conf.d/

# Remove cache files
RUN  rm -rf /var/lib/apt/lists/*

# Copy project files
RUN mkdir -p /srv/www/app & mkdir -p /srv/www/bin & mkdir -p /srv/www/static
ADD requirements.txt /srv/www/app/
RUN pip3 install -r /srv/www/app/requirements.txt
ADD deployenv/bin/ /srv/www/bin/
ADD . /srv/www/app
RUN chmod +x /srv/www/bin/*

# supervisord config file
ADD deployenv/bin/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

CMD /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
