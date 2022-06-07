import argparse

import yaml

from preprocessor import ljspeech, aishell3, libritts, aishell3_libritts


def main(config):
    if "AISHELL3-LibriTTS" in config["dataset"]:
        aishell3_libritts.prepare_align(config)
    elif "LJSpeech" in config["dataset"]:
        ljspeech.prepare_align(config)
    elif "AISHELL3" in config["dataset"]:
        aishell3.prepare_align(config)
    elif "LibriTTS" in config["dataset"]:
        libritts.prepare_align(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="path to preprocess.yaml")
    args = parser.parse_args()

    config = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    main(config)
