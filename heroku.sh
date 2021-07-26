echo "HEROKU_APP: " & read HEROKU_APP
echo "SECRET_KEY: " & read SECRET_KEY
heroku login
# heroku create "$HEROKU_APP"
heroku git:remote -a "$HEROKU_APP"
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY="$SECRET_KEY"
git push heroku main
heroku ps:scale web=1
heroku run py manage.py migrate
heroku run py manage.py createsuperuser

exit 0