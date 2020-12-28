echo "for remote origin and heroku"

git add .

read -p "commit description: " description

git commit -m "$description"


declare -a repositories=("origin" "heroku")

for repo in "${repositories[@]}"
do
   git push "$repo" master
 
done

