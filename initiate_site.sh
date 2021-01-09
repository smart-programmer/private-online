echo "running site scripts"


read -p "server type <1 for production : 2 for local>: " server_type


if [ $server_type -eq 2 ]
then
    rm -rf migrations
    python drop_database.py $server_type
    python manage.py db init
    python manage.py db migrate 
    python manage.py db upgrade
    python create_first_admin.py $server_type
    python create_site_settings.py $server_type
else
    python drop_database.py $server_type
    python manage.py db upgrade
    python create_first_admin.py $server_type
    python create_site_settings.py $server_type
fi


