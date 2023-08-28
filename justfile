dev:
    cd frontend && npm run dev

build:
    cd frontend && npm run build

docker-build:
    docker build --tag codeguessr-api .    

docker-serve port="8001":
    docker run \
        --rm \
        --detach \
        --name "codeguessr-api" \
        -v ./rosettacodes.db:/app/rosettacodes.db \
        -p {{port}}:80 \
        codeguessr-api:latest

docker-stop:
    docker container stop codeguessr-api

docker-clean:
    docker rmi codeguessr-api:latest
