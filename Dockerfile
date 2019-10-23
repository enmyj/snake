FROM continuumio/miniconda3
EXPOSE 8000

COPY environment.yml environment.yml
RUN /opt/conda/bin/conda env update --file environment.yml

RUN useradd -ms /bin/bash snake
USER snake
WORKDIR /home/snake

COPY --chown=snake:snake snake.py /home/snake/snake.py

CMD ["uvicorn","snake:app","--host","0.0.0.0","--port","8000"]
