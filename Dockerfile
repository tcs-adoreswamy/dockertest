FROM davidlor/python-git-app
EXPOSE 8501

WORKDIR /app
# COPY . /app
# ENV ChocolateyUseWindowsCompression false 
# RUN Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force
# RUN -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
# RUN choco install git.install -y --no-progress

RUN git clone https://github.com/tcs-adoreswamy/dockertest .

# WORKDIR /app/dockertest
RUN pip install -r requirements.txt
RUN pip install streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
