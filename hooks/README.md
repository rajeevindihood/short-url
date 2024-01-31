This directory contains hooks that will be executed in DockerHub's AutoBuild environment

[Official Docs](https://docs.docker.com/docker-hub/builds/advanced/#override-build-test-or-push-commands)

pre_build - This is run before the container is built
post_push - This is run after AutoBuild has pushed the image. This step is only run when executing a build rule or Automated build
