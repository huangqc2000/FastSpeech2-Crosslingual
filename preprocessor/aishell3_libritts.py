import os

import librosa
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm
import yaml

from text import _clean_text


def prepare_aishell3(config):
    in_dir = config["path"]["AISHELL3_path"]
    out_dir = config["path"]["raw_path"]
    sampling_rate = config["preprocessing"]["audio"]["sampling_rate"]
    max_wav_value = config["preprocessing"]["audio"]["max_wav_value"]
    for dataset in ["train", "test"]:
        print("Processing {}ing set...".format(dataset))
        with open(os.path.join(in_dir, dataset, "content.txt"), encoding="utf-8") as f:
            for line in tqdm(f):
                wav_name, text = line.strip("\n").split("\t")
                speaker = wav_name[:7]
                text = text.split(" ")[1::2]
                wav_path = os.path.join(in_dir, dataset, "wav", speaker, wav_name)
                if os.path.exists(wav_path):
                    os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)
                    wav, _ = librosa.load(wav_path, sampling_rate)
                    wav = wav / max(abs(wav)) * max_wav_value
                    wavfile.write(
                        os.path.join(out_dir, speaker, wav_name),
                        sampling_rate,
                        wav.astype(np.int16),
                    )
                    with open(
                            os.path.join(out_dir, speaker, "{}.lab".format(wav_name[:11])),
                            "w",
                    ) as f1:
                        f1.write(" ".join(text))


def prepare_libritts(config):
    in_dir = config["path"]["LibriTTS_path"]
    out_dir = config["path"]["raw_path"]
    sampling_rate = config["preprocessing"]["audio"]["sampling_rate"]
    max_wav_value = config["preprocessing"]["audio"]["max_wav_value"]
    cleaners = config["preprocessing"]["text"]["en_text_cleaners"]
    for speaker in tqdm(os.listdir(in_dir)):
        for chapter in os.listdir(os.path.join(in_dir, speaker)):
            for file_name in os.listdir(os.path.join(in_dir, speaker, chapter)):
                if file_name[-4:] != ".wav":
                    continue
                base_name = file_name[:-4]
                text_path = os.path.join(
                    in_dir, speaker, chapter, "{}.normalized.txt".format(base_name)
                )
                wav_path = os.path.join(
                    in_dir, speaker, chapter, "{}.wav".format(base_name)
                )
                with open(text_path) as f:
                    text = f.readline().strip("\n")
                text = _clean_text(text, cleaners)

                os.makedirs(os.path.join(out_dir, speaker), exist_ok=True)
                wav, _ = librosa.load(wav_path, sampling_rate)
                wav = wav / max(abs(wav)) * max_wav_value
                wavfile.write(
                    os.path.join(out_dir, speaker, "{}.wav".format(base_name)),
                    sampling_rate,
                    wav.astype(np.int16),
                )
                with open(
                        os.path.join(out_dir, speaker, "{}.lab".format(base_name)),
                        "w",
                ) as f1:
                    f1.write(text)


def prepare_align(config):
    prepare_aishell3(config)
    prepare_libritts(config)

# if __name__ == '__main__':
#     config = yaml.load(open("./config/AISHELL3-LibriTTS/preprocess.yaml", "r"), Loader=yaml.FullLoader)
#     # prepare_aishell3(config)
#     prepare_libritts(config)
