import time
import pickle
import logging
from pathlib import Path

from torch.utils.data import Dataset
from torchvision.io import read_image
from torchvision.transforms import transforms

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

emotions = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
positive_emotions = ["happy", "neutral", "surprise"]
NUM_CLASSES = len(emotions)

# TODO: add random transformation
train_transform = transforms.Compose([transforms.ToPILImage(),
                                      transforms.Grayscale(num_output_channels=1),
                                      transforms.RandomPerspective(distortion_scale=0.1),
                                      transforms.RandomHorizontalFlip(p=0.5),
                                      transforms.RandomRotation(degrees=(-10,10), fill=50),
                                      transforms.RandomResizedCrop(48, scale=(0.9,1.0), ratio=(0.9, 1.1)),
                                      transforms.ToTensor(),
                                      transforms.Normalize((0.5,), (0.5,))
])

#이미지 텐서를 -1 에서 1 로 정규화   
normalize_transform = transforms.Compose([transforms.ToPILImage(),
                                        transforms.ToTensor(),
                                          transforms.Normalize((0.5,), (0.5,))
])

class FER13(Dataset):
    """Dataset object for https://www.kaggle.com/msambare/fer2013"""
    def __init__(self, path):
        self.images = []
        self.labels = []
        for label, emotion in enumerate(emotions):
            emotion_dir = path.joinpath(emotion)
            for file_path in emotion_dir.iterdir():       
                img_tensor = normalize_transform(read_image(str(file_path)))
                self.images.append(img_tensor)
                self.labels.append(label)

    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]
    
    def __len__(self):
        return len(self.labels)

def load_and_cache_dataset(dataset_path):
    """캐시 된 데이터셋이 있으면 가져오고 없으면 로드해서 캐시에 저장"""
    logging.info("Start loading datasest.")
    start = time.time()    
    
    train_cache_path = dataset_path.joinpath("train.pkl")
    test_cache_path = dataset_path.joinpath("test.pkl")

    # Train 셋    
    if train_cache_path.exists():
        logging.info("Use cache training file.")
        with open(train_cache_path, "rb") as f:
            train_dataset = pickle.load(f)
    else:
        train_dataset = FER13(dataset_path.joinpath("train/")) 
        with open(train_cache_path, "wb") as f:
            pickle.dump(train_dataset, f)
    
    # 테스트 셋
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