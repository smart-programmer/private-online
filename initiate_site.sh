echo "running site scripts"


read -p "server type <1 for production : 2 for local>: " server_type



python reset_database.py $server_type
python create_first_admin.py $server_type
python create_site_settings.py $server_type
