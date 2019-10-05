FROM continuumio/miniconda3:latest

RUN useradd -ms /bin/bash snake
USER snake
WORKDIR /home/snake

COPY environment.yml environment.yml
COPY snake.py snake.py

RUN /opt/conda/bin/conda env create -f environment.yml
RUN /opt/conda/bin/conda activate snake

CMD ["uvicorn", "snake:app"]
