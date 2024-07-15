import os

from vits import utils


def modelLoader():
    modelDll = {}
    # print(type(a))
    ind = 0
    CHOISE = {}
    modelSelect = []

    for i in os.listdir('vits/voiceModel'):
        if os.path.isdir(f'vits/voiceModel/{i}'):
            # 内层循环遍历取出模型文件
            for ass in os.listdir(f'vits/voiceModel/{i}'):
                if ass.endswith('.pth'):
                    hps_ms = utils.get_hparams_from_file(f'vits/voiceModel/{i}/config.json')
                    speakers = hps_ms.speakers if 'speakers' in hps_ms.keys() else ['0']
                    muspeakers = {}
                    for id, name in enumerate(speakers):
                        muspeakers[str(id)] = name
                        CHOISE[name] = [str(id),
                                        [f'vits/voiceModel/{i}/{ass}', f'vits/voiceModel/{i}/config.json']]

                    modelDll[str(ind)] = [f'vits/voiceModel/{i}/{ass}', f'vits/voiceModel/{i}/config.json',
                                          muspeakers]
                    modelSelect = [f'vits/voiceModel/{i}/{ass}', f'vits/voiceModel/{i}/config.json',
                                   muspeakers]

                    # print(time + '| 已读取' + 'voiceModel/' + i + '文件夹下的模型文件' + str(muspeakers))
                    ind += 1

    return modelDll, modelSelect, CHOISE
