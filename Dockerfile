FROM python:3

ADD player_order.py /
ADD .env /

RUN pip install discord.py
RUN pip install python-dotenv


CMD python /player_order.py