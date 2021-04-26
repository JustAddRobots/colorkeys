FROM centos:7.9.2009
ENV TZ=America/Los_Angeles

ARG GIT_COMMIT="${GIT_COMMIT}"
ARG ENGCOMMON_BRANCH="${ENGCOMMON_BRANCH}"
ENV DEBUG=""
ENV JSON=""
ENV PLOT=""
ENV N_CLUSTERS=""
ENV IMAGES=""
ENV PATH="${PATH}:/root/.local/bin"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    yum -y install \
    git \
    python3 \
    && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    ENGCOMMON_BRANCH=$ENGCOMMON_BRANCH python3 -m pip install --user --force-reinstall git+https://github.com/JustAddRobots/colorkeys.git@$GIT_COMMIT && \
    rm -rf ~/.cache/pip && \
    yum -y remove \
    git \
    && \
    yum clean all && rm -rf /var/cache/yum

CMD colorkeys $DEBUG $JSON $PLOT $N_CLUSTERS $IMAGES
