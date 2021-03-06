#############################################################
#############################################################

### dataset.py: 데이터 셋을 불러오고, 캐시에 저장합니다.

#############################################################
#############################################################

import time
import pickle
import logging
from pathlib import Path

import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.io import read_image
from torchvision.datasets import ImageFolder
from torchvision.transforms import transforms

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

emotions = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
positive_emotions = ["happy", "neutral", "surprise"]
NUM_CLASSES = len(emotions)

# TODO: add random transformation
'''
train_transform = transforms.Compose([transforms.ToPILImage(),
                                       #transforms.Grayscale(num_output_channels=1),
                                      transforms.RandomPerspective(distortion_scale=0.1),
                                      transforms.RandomHorizontalFlip(p=0.5),
                                      transforms.RandomRotation(degrees=(-10,10), fill=50),
                                      transforms.RandomResizedCrop(48, scale=(0.9,1.0), ratio=(0.9, 1.1)),
                                      transforms.ToTensor(),
                                      transforms.Normalize((0.5,), (0.5,))
])
'''

val_transform = transforms.Compose([transforms.ToPILImage(),#transforms.Grayscale(num_output_channels=1),
                                    transforms.ToTensor(),
                                    transforms.Normalize((0.5,), (0.5,))
])

# 이미지 텐서를 -1 에서 1 로 정규화 
normalize_transform = transforms.Compose([transforms.ToPILImage(),
                                        transforms.ToTensor(),
                                          transforms.Normalize((0.5,), (0.5,))
])
#print(normalize_transform(read_image("./FER-2013/train/angry/PrivateTest_88305.jpg")))
def transform(img_tensor):
    """이미지 텐서를 -1 에서 1 로 정규화"""
    return torch.Tensor((img_tensor/255.0 - 0.5)*2) 

class FER13(Dataset):
    """데이터셋에서 이미지 파일을 읽어오는 역할"""
    """Dataset object for https://www.kaggle.com/msambare/fer2013"""
    def __init__(self, path):
        self.images = []
        self.labels = []
        for label, emotion in enumerate(emotions):
            emotion_dir = path.joinpath(emotion)
            for file_path in emotion_dir.iterdir():      

                # 원활한 학습을 위해 -1과 1 사이로 정규화
                # normalize_transform 호출
                img_tensor = normalize_transform(read_image(str(file_path)))
                
                #img_tensor = transform(read_image(str(file_path)))
                self.images.append(img_tensor)
                self.labels.append(label)

    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]
    
    def __len__(self):
        return len(self.labels)

# 이미지 파일 캐싱 (train.pkl)
def load_and_cache_dataset(dataset_path):
    """캐시 된 데이터셋이 있으면 가져오고 없으면 로드해서 캐시에 저장"""
    logging.info("Start loading datasest.")
    start = time.time()    
    
    train_cache_path = dataset_path.joinpath("train.pkl")
    test_cache_path = dataset_path.joinpath("test.pkl")

    # Train 셋 
    # 또 학습을 할 일이 있다면 train.pkl 파일을 가져와서 사용   
    if train_cache_path.exists():
        logging.info("Use cache training file.")
        with open(train_cache_path, "rb") as f:
            train_dataset = pickle.load(f)
    else:
        train_dataset = FER13(dataset_path.joinpath("train/")) 
        with open(train_cache_path, "wb") as f:
            pickle.dump(train_dataset, f)
    
    # 테스트 셋 (Train 셋과 동일)
    if test_cache_path.exists():
        logging.info("Use cache test file.")
        with open(test_cache_path, "rb") as f:
            test_dataset = pickle.load(f)
    else:
        test_dataset = FER13(dataset_path.joinpath("test/"))
        with open(test_cache_path, "wb") as f:
            pickle.dump(test_dataset, f)

    logging.info(f"End loading dataset. {time.time()-start:.2f} sec")
    return train_dataset, test_dataset

if __name__ == "__main__":
    load_and_cache_dataset(Path("./FER-2013"))

# file end