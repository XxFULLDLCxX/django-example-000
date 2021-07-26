requirements="django environs[django] psycopg2-binary whitenoise gunicorn"
[ "$1" == '' ] && echo "Env: requirements for install all requirements."
[ "$1" == 'requirements' ] && pipenv install $requirements
[ "$1" != 'requirements' ] && pipenv $@

exit 0