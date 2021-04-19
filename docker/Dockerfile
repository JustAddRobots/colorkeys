FROM centos:7.9.2009
ENV TZ=America/Los_Angeles
ENV DEBUG=""
ENV JSON=""
ENV PLOT=""
ENV N_CLUSTERS=""
ENV IMAGES=""
ARG GIT_COMMIT="dev"
ARG ENGCOMMON_BRANCH="main"
ENV PATH="${PATH}:/root/.local/bin"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    yum -y install \
    git \
    mesa-libGL \
    python3 \
    && \
    yum clean all && rm -rf /var/cache/yum

RUN python3 -m pip install --upgrade pip setuptools && \
    ENGCOMMON_BRANCH=$ENGCOMMON_BRANCH CFLAGS="-Os -g0 -Wl,--strip-all" python3 -m pip install --no-cache-dir --compile --global-option=build_ext --user --force-reinstall git+https://github.com/JustAddRobots/colorkeys.git@$GIT_COMMIT && \
    rm -rf ~/.cache/pip

CMD colorkeys $DEBUG $JSON $PLOT $N_CLUSTERS $IMAGES
