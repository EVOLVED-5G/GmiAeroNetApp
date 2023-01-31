# 
FROM python:3.10.1

# 
WORKDIR /code

# 
COPY ./src /code/src

#
ENV PYTHONPATH "${PYTHONPATH}:/code/src"

# 
COPY ./requirements.txt /code/requirements.txt

#install jq
RUN apt-get update && apt-get install -y jq && apt-get clean

#
RUN mkdir -p /code/src/capif_onboarding

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8383

#run prpeare.sh script to register Capif and start the NetApp
CMD ["sh", "/code/src/prepare.sh"]