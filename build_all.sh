echo "Building all"
cd carbone-api
bash build.sh
cd ..

cd carbone-app
bash build.sh
cd ..

cd server
bash build.sh
cd ..
