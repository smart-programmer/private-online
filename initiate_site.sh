echo "running site scripts"




if [ $1 -eq 2 ]
then
    rm -rf migrations
    python drop_database.py $1
    python manage.py db init
    python manage.py db migrate 
    python manage.py db upgrade
    python create_first_admin.py $1
    python create_site_settings.py $1
    python create_users.py $1
    python create_adminstration_storage.py $1
else
    python reset_database.py $1
    python manage.py db upgrade
    python create_first_admin.py $1
    python create_site_settings.py $1
    python create_adminstration_storage.py $1
fi


