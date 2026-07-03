import os
import cv2
import argparse
from tqdm import tqdm


def extract_frames(video_path, output_folder, target_fps=24):
    """
    Extract frames from a video at the specified FPS.
    Frames are saved as lossless PNG images.
    """

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found:\n{video_path}")

    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError("Unable to open video.")

    source_fps = cap.get(cv2.CAP_PROP_FPS)

    if source_fps <= 0:
        raise RuntimeError("Unable to determine video FPS.")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = total_frames / source_fps

    total_output_frames = int(duration * target_fps)

    print(f"\nVideo           : {video_path}")
    print(f"Resolution      : {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))} x {int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    print(f"Original FPS    : {source_fps:.2f}")
    print(f"Target FPS      : {target_fps}")
    print(f"Duration        : {duration:.2f} sec")
    print(f"Frames to Save  : {total_output_frames}\n")

    progress = tqdm(total=total_output_frames)

    saved = 0

    while True:

        timestamp = saved / target_fps

        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)

        success, frame = cap.read()

        if not success:
            break

        filename = os.path.join(
            output_folder,
            f"frame_{saved:06d}.png"
        )

        cv2.imwrite(
            filename,
            frame,
            [
                cv2.IMWRITE_PNG_COMPRESSION,
                0,  # 0 = No compression (highest quality)
            ],
        )

        saved += 1
        progress.update(1)

    progress.close()
    cap.release()

    print("\nDone!")
    print(f"Saved {saved} frames")
    print(f"Output folder:\n{os.path.abspath(output_folder)}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Extract video frames at a fixed FPS."
    )

    parser.add_argument(
        "video",
        help="Path to input video"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="frames_24fps",
        help="Output folder"
    )

    parser.add_argument(
        "--fps",
        type=float,
        default=24,
        help="Target FPS (default: 24)"
    )

    args = parser.parse_args()

    extract_frames(
        args.video,
        args.output,
        args.fps
    )