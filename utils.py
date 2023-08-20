import glob
import random
import time
import copy
from tqdm import tqdm

from collections import defaultdict


SINGING_VOICE_SEEN_DATASETS = ["m4singer", "opencpopbeta", "pjs"]
SINGING_VOICE_UNSEEN_DATASETS = ["opencpop", "opensinger", "csd", "popcs"]
SPEECH_SEEN_DATASETS = ["libritts", "ljspeech"]
SPEECH_UNSEEN_DATASETS = ["vctk"]

SINGING_VOICE_MOS_SETTINGS = [
    "gt",
    "hifigan_orig",
    "hifigan_merge",
    "hifigan_mscqtd",
    "hifigan_msstftd",
]

SPEECH_MOS_SETTINGS = [
    "gt_speech",
    "hifigan_orig_speech",
    "hifigan_merge_speech",
    "hifigan_mscqtd_speech",
    "hifigan_msstftd_speech",
]

PREFERENCE_SETTINGS = [
    ["melgan_orig", "melgan_merge"],
    ["bigvgan_orig", "bigvgan_merge"],
    ["nsfhifigan_orig", "nsfhifigan_merge"],
]


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def parse_uid_from_audio_path(wav_file):
    uid = wav_file.split("/")[-1].split(".wav")[0]
    return uid


def parse_dataset_from_audio_path(wav_file):
    speaker = wav_file.split("/")[-2]
    return speaker


def parse_system_from_audio_path(wav_file):
    system = wav_file.split("/")[-3]
    return system


def parse_uids_from_datasets(seen_unseen, category):
    if category == "singing":
        if seen_unseen == "seen":
            datasets = copy.deepcopy(SINGING_VOICE_SEEN_DATASETS)
        else:
            datasets = copy.deepcopy(SINGING_VOICE_UNSEEN_DATASETS)
    else:
        if seen_unseen == "seen":
            datasets = copy.deepcopy(SPEECH_SEEN_DATASETS)
        else:
            datasets = copy.deepcopy(SPEECH_UNSEEN_DATASETS)
    result = []

    for dataset in datasets:
        dataset_uids = []
        uids = copy.deepcopy(dataset_uid_dict[dataset])
        for uid in uids:
            dataset_uids.append("{}${}".format(dataset, uid))
        result = result + dataset_uids

    return copy.deepcopy(result)


dataset_uid_dict = defaultdict()

folders = glob.glob("static/data/*")
for folder in folders:
    if not folder.split("/")[-1] in ["gt", "gt_speech"]:
        continue
    wave_files = glob.glob("{}/*/*.wav".format(folder))
    for wave_file in wave_files:
        dataset = parse_dataset_from_audio_path(wave_file)
        uid = parse_uid_from_audio_path(wave_file)
        if not dataset in dataset_uid_dict.keys():
            dataset_uid_dict[dataset] = []
        dataset_uid_dict[dataset].append(uid)

SINGING_VOICE_SEEN_UIDS = parse_uids_from_datasets("seen", "singing")
SINGING_VOICE_UNSEEN_UIDS = parse_uids_from_datasets("unseen", "singing")
SPEECH_SEEN_UIDS = parse_uids_from_datasets("seen", "speech")
SPEECH_UNSEEN_UIDS = parse_uids_from_datasets("unseen", "speech")

# print(len(SINGING_VOICE_SEEN_UIDS))
# print(len(SINGING_VOICE_UNSEEN_UIDS))
# print(len(SPEECH_SEEN_UIDS))
# print(len(SPEECH_UNSEEN_UIDS))


def get_mos_test_audio(seen_unseen, category):
    if category == "singing":
        settings = copy.deepcopy(SINGING_VOICE_MOS_SETTINGS)
        if seen_unseen == "seen":
            uids = copy.deepcopy(SINGING_VOICE_SEEN_UIDS)
        else:
            uids = copy.deepcopy(SINGING_VOICE_UNSEEN_UIDS)
    else:
        settings = copy.deepcopy(SPEECH_MOS_SETTINGS)
        if seen_unseen == "seen":
            uids = copy.deepcopy(SPEECH_SEEN_UIDS)
        else:
            uids = copy.deepcopy(SPEECH_UNSEEN_UIDS)
    test_audios = []
    random.shuffle(settings)

    idx = random.randint(0, len(uids) - 1)
    dataset_uid = uids[idx]
    dataset, uid = dataset_uid.split("$")

    for setting in settings:
        if not setting in ["gt", "gt_speech"]:
            path = "static/data/{}/{}/{}_pred.wav".format(setting, dataset, uid)
        else:
            path = "static/data/{}/{}/{}.wav".format(setting, dataset, uid)
        test_audios.append(path)

    return test_audios


def get_preference_test_audio(seen_unseen, idx):
    settings = copy.deepcopy(PREFERENCE_SETTINGS[idx])
    if seen_unseen == "seen":
        uids = copy.deepcopy(SINGING_VOICE_SEEN_UIDS)
    else:
        uids = copy.deepcopy(SINGING_VOICE_UNSEEN_UIDS)
    test_audios = []
    random.shuffle(settings)
    settings.append("gt")

    idx = random.randint(0, len(uids) - 1)
    dataset_uid = uids[idx]
    dataset, uid = dataset_uid.split("$")

    for setting in settings:
        if not setting in ["gt", "gt_speech"]:
            path = "static/data/{}/{}/{}_pred.wav".format(setting, dataset, uid)
        else:
            path = "static/data/{}/{}/{}.wav".format(setting, dataset, uid)
        test_audios.append(path)

    return test_audios
