# Requirement

- Click=7.0
- Flask=1.0.3

- Flask-Script=2.0.6
- itsdangerous=1.1.0
- Jinja2=2.10.1
- MarkupSafe=1.1.1
- Werkzeug=0.15.4

conda create -n env_passport python=3.6
source activate env_passport
conda install flask
conda install --channel https://conda.anaconda.org/conda-forge flask-script
conda install --channel https://conda.anaconda.org/joshbtn neo4j-driver
conda install --channel https://conda.anaconda.org/anaconda neotime
conda install xlwt
conda install mysql
conda install paramiko
conda install --channel https://conda.anaconda.org/conda-forge uwsgi
conda install requests
conda install mysqlclient

# setup:

source activate env_health

单进程:
python manage.py runserver

多进程:nginx + uwsgi + flask
uwsgi uwsgi.ini


可以用 ps aux | grep uwsgi 查看uwsgi工作情况
killall -9 uwsgi 可以终止守护进程


(killall -9 uwsgi)+(uwsgi uwsgi.ini)=>./restart.sh

nginx重启：sudo service nginx restart