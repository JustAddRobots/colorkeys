#!/usr/bin/env python3

import datetime
import ffmpeg
import logging
import numpy as np
import os

from engcommon import command

logger = logging.getLogger(__name__)


def check_ffmpeg():
    """Check if ffpmeg can be called."""
    cmd = "ffmpeg -version"
    command.call_shell_cmd(cmd)
    return None


def extract_frames(video_file, start, end, out_dir, spf=1):
    """Extract frames from video file to output directory.

    Extract frames using start and end timecodes. Uses ffmpeg to extract
    frames to PNG format.

    Args:
        video_file (str): Input video file name.
        start (str): Timecode to start the extraction in HH:MM:SS.
        end (str): Timecode to end the extraction in HH:MM:SS.
        out_dir (str): Output directory for extracted frames.
        spf (int): Seconds per frame; seconds between each frame extraction.

    Returns:
        None
    """
    check_ffmpeg()
    # Get seek positions based on start/end and seconds per frame
    dt = datetime.datetime.now()
    timestamp = (
        f"{dt.year}.{dt.month:02d}.{dt.day:02d}-"
        f"{dt.hour:02d}{dt.minute:02d}{dt.second:02d}"
    )
    secs_start = get_seconds(start)
    secs_end = get_seconds(end)
    secs_duration = secs_end - secs_start
    num_frames = secs_duration // spf
    seek_positions = np.around(
        np.linspace(secs_start, secs_end, num_frames, endpoint=False),
        decimals = 3
    ).tolist()

    # Extract frames to directory
    filmtitle = os.path.splitext(os.path.basename(video_file))[0]
    extract_dir = f"{out_dir}/{filmtitle}/{timestamp}"
    os.makedirs(extract_dir)
    logger.debug(f"Extracting {video_file} to {extract_dir}")
    for pos in seek_positions:
        _, _ = (
            ffmpeg
            .input(video_file, ss=pos)
            .output(f"{extract_dir}/{filmtitle}-{pos:.2f}.png", vframes=1)
            .run(quiet=True)
        )
    logger.debug(f"Extracted {video_file} to {extract_dir}")
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
    check_ffmpeg()
    p = ffmpeg.probe(filename)
    v = next(
        (stream for stream in p['streams'] if stream['codec_type'] == 'video'),
        None
    )
    return eval(v["r_frame_rate"])
