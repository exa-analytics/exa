FROM tensorflow/tensoflow:2.0.0-py3
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN useradd -ms /bin/bash exa-user
