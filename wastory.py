import os
import sys
from math import ceil
import ffmpeg
import typer

app = typer.Typer()


@app.command()
def main(path: str):
    filename, file_extension = os.path.splitext(os.path.basename(path))
    directory = os.path.dirname(path)
    print(f"Processing {filename}{file_extension} ...")
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        print('No video stream found', file=sys.stderr)
        sys.exit(1)
    fileinput = ffmpeg.input(path)
    video = fileinput.video
    audio = fileinput.audio
    duration = int(float(video_stream['duration']))
    start = 0

    i = 1
    while start < duration:
        print(f"Loading... ({i}/{ceil(duration/29)})")
        cut(video, audio, start, filename, i)
        i = i + 1
        start = start+29
    return True


def cut(video, audio, start, filename, i):
    video = video.filter('trim', start=start, duration=29).filter('setpts', 'PTS-STARTPTS')
    audio = audio.filter('atrim', start=start, duration=29).filter('asetpts', 'PTS-STARTPTS')
    ffmpeg.output(audio, video, f"{filename}_{i}.mp4", format='mp4').overwrite_output().run(capture_stdout=True, capture_stderr=True)


if __name__ == '__main__':
    app()
