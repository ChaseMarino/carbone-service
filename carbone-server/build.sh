docker build -f Dockerfile .

GCREPO="registry.gitlab.com/{REPO}/gitlabregistries"
LOCALCONT="carbone-server:latest"

docker build -t $LOCALCONT -f Dockerfile .
docker tag $LOCALCONT $GCREPO/$LOCALCONT
docker push $GCREPO/$LOCALCONT
