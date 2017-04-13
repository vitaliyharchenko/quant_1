Quant.zone
==========

Наше LMS приложение

**Requirements for local development:** Python 3.6, PostgreSQL, Gulp, NodeJS, Graphviz

## Local dev:

1. Git clone

    ```
    ssh root@188.127.249.128
    oGWRAKrle8so
    git clone -b dev https://github.com/vitaliyharchenko/quantzone.git
    ```

2. [Install Docker on Ubuntu 16.04 x64](https://docs.docker.com/engine/installation/linux/ubuntu/)

3. [Install Docker Compose](https://docs.docker.com/compose/install/)

4. Specify env file, etc:

   ```
   DB_NAME=qdb
   DB_USER=quser
   DB_PASS=4203
   DB_SERVICE=postgres
   DB_PORT=5432

   CURRENT_HOST=0.0.0.0
   ```

3. Build docker containers

    ```
    cd /quantzone
    docker-compose build
    ```

4. For frontend development:

    ```
    docker-compose run web /bin/sh
    # sh prod_run.sh
    ```

https://oauth.vk.com/authorize?client_id=5551024&display=popup&redirect_uri=http://0.0.0.0/user/update&response_type=code&v=5.41
https://oauth.vk.com/access_token?client_id=5551024&client_secret=8C6BjXZii7PDzryIX2QG&redirect_uri=127.0.0.1:8000/login


3. Install Graphvis (http://django-extensions.readthedocs.io/en/latest/graph_models.html)

    ```
    pip install pygraphvis --install-option="--include-path=/usr/local/include/graphviz/" \
    --install-option="--library-path=/usr/local/lib/graphviz"
    pip install pydotplus
    ```

### Frontend:

1. Load requirements

    ```
    npm install
    ```

2. Start Gulp

    ```
    gulp
    ```

3. That's it -- you're done!

    
### Advices

1. Work in coding style: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/

```
isort -rc .
```

2. 