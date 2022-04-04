# 
FROM python:3.9

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
RUN pip install requests

# 
CMD ["uvicorn", "src.main:app", "--port", "8000"]