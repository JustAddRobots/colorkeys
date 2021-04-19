FROM centos:7.9.2009
ENV TZ=America/Los_Angeles
ENV DEBUG=""
ENV JSON=""
ENV PLOT=""
ENV N_CLUSTERS=""
ENV IMAGES=""
ARG GIT_COMMIT="master"
ARG ENGCOMMON_BRANCH="${ENGCOMMON_BRANCH}"
ENV PATH="${PATH}:/root/.local/bin"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    yum -y install \
    git
    mesa-libGL
    python3
    && \
    yum clean all && rm -rm /var/cache/yum && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    ENGCOMMON_BRANCH=$ENGCOMMON_BRANCH python3 -m pip install --user --force-reinstall git+https://github.com/JustAddRobots/colorkeys.git@GIT_COMMIT && \
    rm -rm ~/.cache/pip

CMD colorkeys $DEBUG $JSON $PLOT $N_CLUSTERS $IMAGES
