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
EXPOSE 8000

# 
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]