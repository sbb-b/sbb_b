FROM jmthonar/jmthon:slim-buster

#clonning repo 
RUN git clone https://github.com/jmthonar/jmthon.git /root/jmthon
#working directory 
WORKDIR /root/jmthon

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/jmthon/bin:$PATH"

CMD ["python3","-m","jmthon"]
