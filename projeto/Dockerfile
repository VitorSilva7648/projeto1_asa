FROM python
RUN apt-get update && apt-get install python3-pip -y
WORKDIR /projeto_01_beta
COPY . /projeto_01_beta/
RUN pip install -r requirements.txt 
CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "5000"] 