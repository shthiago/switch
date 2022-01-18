#! /bin/bash
# Setup Docker running Neo4j, with the neosemantics extension and if the dataset is ready, load it

CONTAINERNAME=$1

echo "Downloading neosemantics"
mkdir -p neo4j/plugins/
mkdir -p dataset
wget https://github.com/neo4j-labs/neosemantics/releases/download/4.4.0.0/neosemantics-4.4.0.0.jar -P neo4j/plugins/

echo "Running docker image"
docker run  --name $CONTAINERNAME \
            -p7474:7474 -p7687:7687 \
            -d \
            -v $(pwd)/neo4j/data:/data \
            -v $(pwd)/neo4j/logs:/logs \
            -v $(pwd)/neo4j/import:/var/lib/neo4j/import \
            -v $(pwd)/neo4j/plugins:/var/lib/neo4j/plugins \
            -v $(pwd)/dataset/:/dataset \
            --env NEO4J_AUTH=none \
            neo4j:latest
sleep 5

echo "Setting up neosemantics"
docker exec $CONTAINERNAME bash -c 'echo "dbms.unmanaged_extension_classes=n10s.endpoint=/rdf" >> /var/lib/neo4j/conf/neo4j.conf && neo4j restart'
sleep 15
docker exec $CONTAINERNAME bash -c 'echo "CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;" | cypher-shell'
docker exec $CONTAINERNAME bash -c 'echo "CALL n10s.graphconfig.init();" | cypher-shell'

if test -f "dataset/dataset.rdf"; then
    echo "Loading dataset"
    docker exec $CONTAINERNAME bash -c 'echo "CALL n10s.rdf.import.fetch(\"file:///dataset/dataset.rdf\", \"RDF/XML\");" | cypher-shell'
else
    echo "Dataset not ready"
fi

echo "Done!"