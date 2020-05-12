#!/bin/bash
# This script will start the pipeline and give the user access to the text-based menu options.

# The created container is named pipeline.
# The container starts a bash session.
# The container has the "pipeline" folder mounted, and is made accessible at location "StopSpot_Data_Pipeline"
# The container will be deleted when it stops running.
# The tag "pipetag" is searched for as a base image for creating this container.

sudo docker run -d -it \
	--name pipeline \
	--entrypoint "/bin/bash" \
	--mount type=bind,source="$(pwd)"/pipeline,target=/StopSpot_Data_Pipeline \
	--rm \
	pipetag

sudo docker exec -it pipeline python3 main.py

sudo docker stop pipeline