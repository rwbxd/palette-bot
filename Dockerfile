FROM python:3.12.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV DISCORD_TOKEN="DISCORD_BOT_TOKEN"
ENV GUILD_ID="GUILD_ID"
ENV PYTHONUNBUFFERED=1

COPY . .
CMD python bot.py $GUILD_ID
