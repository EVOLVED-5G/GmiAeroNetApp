# 
FROM python:3.10.1

# 
WORKDIR /code

# 
COPY ./src /code/src

ENV PYTHONPATH "${PYTHONPATH}:/code/src"

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install evolved5g
RUN pip install uvicorn
RUN pip install pydantic
RUN pip install aiofiles

EXPOSE 8383


CMD ["sh", "/code/src/prepare.sh"]

