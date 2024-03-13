FROM python:3.9

RUN mkdir /ecommerce

WORKDIR /ecommerce

COPY requirements/base.txt /tmp/base.txt
COPY requirements/prod.txt /tmp/prod.txt

RUN pip install --no-cache-dir -r /tmp/base.txt && \
    pip install --no-cache-dir -r /tmp/prod.txt && \
    rm -rf /tmp

COPY . .

RUN chmod a+x /ecommerce/docker/*.sh

