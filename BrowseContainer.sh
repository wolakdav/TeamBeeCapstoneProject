#!/bin/bash
# This script will allow the user to browse the container and it's file structure
# They'll aslo have the option of potentially invoking the pipeline with an argument.

# The created container is named pipeline.
# The container starts a bash session.
# The container has the "pipeline" folder mounted, and is made accessible at location "StopSpot_Data_Pipeline"
# The container will be deleted when it stops running.
# The tag "pipetag" is searched for as a base image for creating this container.

sudo docker run -it \
	--name pipeline \
	--entrypoint "/bin/bash" \
	--mount type=bind,source="$(pwd)"/pipeline,target=/StopSpot_Data_Pipeline \
	--rm \
	pipetag