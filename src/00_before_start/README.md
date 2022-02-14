# 00_before_start

Before workshop starts please do steps below.

## Required

1. Please install `docker` and `docker-compose` on your system.
    - [Install Docker Engine](https://docs.docker.com/engine/install/#server)
    - [Install Docker Compose](https://docs.docker.com/compose/install/)
2. Clone/download this repo.
3. Check if you can start `docker-compose.yml` services:

    ```script
    ❯ cd conan_workshop
    ❯ docker-compose up -d
    Creating network "conan_workshop_default" with the default driver
    Creating dev         ... done
    Creating artifactory ... done
    ❯ docker logs -f artifactory
    Preparing to run Artifactory in Docker
    Running as uid=1030(artifactory) gid=1030(artifactory) groups=1030(artifactory)
    ...
    ...
    ###############################################################
    ###   All services started successfully in 32.189 seconds   ###
    ###############################################################
    ...
    ^C
    ```

4. If you see above lines you can stop services `docker-compose down` and move
to [Optional](#Optional) section.


## Optional

Optionally you can watch the
[Introduction to Conan](https://academy.jfrog.com/path/conan/introduction-to-conan)
tutorial (~8 min).
