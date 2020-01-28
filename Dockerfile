FROM tensorflow/tensoflow:2.0.0-py3
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN useradd -ms /bin/bash exa-user

WORKDIR /home/exa-user
ENV PYTHONPATH=/home/exa-user

COPY --chown=exa-user exa/ exa/
COPY --chown=exa-user setup.py setup.py

RUN pip install -e .

USER ec2-user
