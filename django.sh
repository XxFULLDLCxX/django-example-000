for i in $@; do
    [ "$i" == '-m' -o "$i" == '-all' ] && (
        python manage.py makemigrations
        python manage.py migrate --run-syncdb)
    [ "$i" == '-#' -o "$i" == '-all' ] && python manage.py createsuperuser
    [ "$i" == '-c' -o "$i" == '-all' ] && python manage.py collectstatic
    [ "$i" == '-d' -o "$i" == '-all' ] && start http://localhost:8000
    [ "$i" == '-r' -o "$i" == '-all' ] && python manage.py runserver
done



[ "$1" == '-A' ] && django-admin ${@: 2}
[ "$1" == '-D' ] && py -m django ${@: 2}
[ "$1" == '-M' ] && py manage.py ${@: 2}

[ "$1" == '' ] && echo -e "./Django.sh Available Commands:
--all         ./Django.sh -m -u -c -d -r
 -A | -D | -M  django-admin | py -m django | py manage.py
 -m            py manage.py makemigrations & py manage.py migrate --run-syncdb
 -u            py manage.py py manage.py createsuperuser
 -c            py manage.py py manage.py collectstatic
 -d            py manage.py start http://localhost:8000
 -r            py manage.py python manage.py runserver"

exit 0