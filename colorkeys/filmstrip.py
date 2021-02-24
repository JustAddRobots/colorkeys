#!/usr/bin/env python3

import datetime
import logging
import numpy as np
import os

from engcommon import command
from engcommon import testvar

logger = logging.getLogger(__name__)


def extract_frames(video_file, start, end, out_dir, spf=1):
    """Extract frames from video file to output directory.

    Extract frames using start and end timecodes. Uses ffmpeg to extract
    frames to PNG format.

    Args:
        video_file (str): Input video file name.
        start (str): Timecode to start the extraction in HH:MM:SS.
        end (str): Timecode to end the extraction in HH:MM:SS.
        out_dir (str): Output directory for extracted frames.
        spf (int): Seconds per frame; seconds between frame extraction.

    Returns:
        None
    """
    dt = datetime.datetime.now()
    timestamp = "{0}.{1:02d}.{2:02d}-{3:02d}{4:02d}{5:02d}".format(
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second
    )
    secs_start = get_seconds(start)
    secs_end = get_seconds(end)
    secs_duration = secs_end - secs_start
    num_frames = secs_duration // spf
    seek_positions = np.around(
        np.linspace(secs_start, secs_end, num_frames, endpoint=False),
        decimals = 3
    ).tolist()
    filmtitle = os.path.splitext(os.path.basename(video_file))[0]
    extract_dir = "{0}/{1}/{2}".format(out_dir, filmtitle, timestamp)
    os.makedirs(extract_dir)
    logger.debug("Extracting {0} to {1}".format(video_file, extract_dir))
    for pos in seek_positions:
        cmd = "ffmpeg -ss {0} -i {1} -frames:v 1 {2}/{3}-{4:.2f}.png".format(
            pos,
            video_file,
            extract_dir,
            filmtitle,
            pos,
        )
        logger.debug(testvar.get_debug(cmd))
        command.call_shell_cmd(cmd)
    logger.debug("Extracted {0} to {1}".format(video_file, extract_dir))
    return None


def get_seconds(timecode):
    """Convert timecode to seconds.

    Args:
        timecode (str): Timecode in HH:MM:SS format.

    Returns:
        secs (int): Timecode in total seconds.
    """
    conv = [3600, 60, 1]  # H:M:S conversion
    secs = sum(
        [a * b for a, b in zip(
            conv, [int(i) for i in timecode.split(":")]
        )]
    )
    return secs


def get_framerate(filename):
    """Get framerate from file information."""
    cmd = (
        "ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 "
        "-show_entries stream=r_frame_rate {0}".format(filename)
    )
    dict_ = command.get_shell_cmd(cmd)
    return eval(dict_["stdout"])
