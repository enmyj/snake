FROM continuumio/miniconda3:latest
EXPOSE 8000

COPY environment.yml environment.yml
RUN /opt/conda/bin/conda env update --file environment.yml

RUN useradd -ms /bin/bash snake
USER snake
WORKDIR /home/snake

COPY --chown=snake:snake snake.py /home/snake/snake.py
COPY --chown=snake:snake starthack.sh /home/snake/starthack.sh

CMD ["uvicorn","snake:app"]
