FROM 09u2/pw4hf

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m -u 1000 user
USER USER

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user app.py models.py browser_actions.py tools.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
