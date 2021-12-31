import os
import json
import time
import pickle
import logging
import datetime
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from model import MiniXception
from dataset import (emotions, positive_emotions, NUM_CLASSES,
                    load_and_cache_dataset, transform, FER13)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    
def load_config(exp_path):
    """config.json 파일 불러오기"""
    config_path = exp_path.joinpath("config.json")
    with open(config_path, 'rt') as f:
        config = json.load(f)
    return config

def load_fer_model(exp_path):
    """저장된 모델 불러오기"""
    config = load_config(exp_path)  
    logging.info(f"Loading {config}")
    model_path = exp_path.joinpath("model.pt")
    model = MiniXception(config["num_classes"], config["eps"], config["momentum"])
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

def inference(model, image):
    """감정, 감정의 확률, 긍정 감정 여부를 반환

    웹 캠에서 이미지 하나를 입력 받아 감정을 판별 할 때 사용
    입력은 (48, 48) 크기의 흑백 numpy 텐서.
    """
    transformed = transform(image)
    transformed = transformed.view(1, 1, 48, 48) # 모델에 맞게 이미지 차원 변환
    
    result = model(transformed) # 이미지를 딥러닝 모델에 입력

    result = result.squeeze() # (1, C) => (C,)
    emotion_idx = result.argmax().item()
    emotion = emotions[emotion_idx] # 가장 높은 확률을 가진 감정

    probs = {emotion:prob for emotion, prob in zip(emotions, result.tolist())}   
    prob = probs[emotion] # 감정 확률
    
    is_pos_emotion = emotion in positive_emotions # 긍정 감정 여부
    return emotion, prob, is_pos_emotion

def evaluate(dataloader, model, loss_fn):
    """Validation loss와 모델 정확도 반환
    
    Test 셋에서 모델 성능 검증
    """
    model.eval()
    total = len(dataloader.dataset)
    num_batches = len(dataloader)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    total_loss = 0
    correct = 0
    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device) # To GPU, if possible
            labels = labels.to(device)
            pred = model(images)

            total_loss += loss_fn(pred, labels).item()
            correct += (pred.argmax(1) == labels).type(torch.float).sum().item()

    val_loss = total_loss / num_batches # Validation loss
    acc = correct / total # 모델의 정확도
    logging.info(f"Val loss: {val_loss:>8f} Acc: {(100*acc):>0.1f}%")
    return val_loss, acc

def train(save_model):
    """트레이닝 셋에서 학습"""
    config = {
        "num_classes": NUM_CLASSES,
        "batch_size": 256,
        "learning_rate": 1e-3,
        "weight_decay": 0.01,
        "momentum": 0.99,
        "eps": 0.001,
        "max_epochs": 40,
        "random_seed": 42,
        "tag": "borm_eps_0.001_moementum_0.09_eval"
    }

    torch.manual_seed(config["random_seed"])
    
    # 데이터셋 불러오기
    dataset_path = Path("./FER-2013/")
    train_dataset, test_dataset = load_and_cache_dataset(dataset_path)
    
    train_dataloader = DataLoader(train_dataset, batch_size=config["batch_size"],
                                  shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=config["batch_size"],
                                 shuffle=True)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MiniXception(config["num_classes"], config["eps"], config["momentum"]) # 딥러닝 모델 생성   
    model.to(device)
    
    # Cross Entropy 손실 함수와 Adam 옵티마이저 사용
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config["learning_rate"],     
                                 weight_decay=config["weight_decay"])
    
    # 학습 시작
    logging.info("Start training.")
    start = time.time()

    early_stopping_count = 0
    last_val_loss = 10**6
    exp_path = None
    for epoch in range(config["max_epochs"]):
        model.train()
        total = len(train_dataloader.dataset)
        for batch, (images, labels) in enumerate(train_dataloader):
            # Compute prediction and loss
            images = images.to(device)
            labels = labels.to(device)
            pred = model(images)
            loss = loss_fn(pred, labels)

            # Backpropagation
            optimizer.zero_grad() # Make gradient of the weights zero
            loss.backward() # Calculate gradient
            optimizer.step() # Update weights

            if batch % 100 == 0:
                loss_val = loss.item()
                current = batch * config["batch_size"]
                logging.info(f"loss: {loss_val:>7f}  [{current:>5d}/{total:>5d}]")

        logging.info(f"Evalution at epoch {epoch}")
        val_loss, acc = evaluate(test_dataloader, model, loss_fn)
        
        # Early stopping
        if val_loss > last_val_loss:
            early_stopping_count += 1
        else:
            early_stopping_count = 0
            saved_acc = acc
            saved_params = model.state_dict()
            # 모델 저장
            if save_model:
                if exp_path is not None:
                    model_path.unlink()
                    config_path.unlink()
                    exp_path.rmdir()

                now = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                exp_path = Path(f"./models/{now}-{saved_acc:.4f}-{config['tag']}")
                exp_path.mkdir(parents=True, exist_ok=True)

                model_path = exp_path.joinpath("model.pt")
                torch.save(saved_params, model_path)

                config_path = exp_path.joinpath("config.json")
                with open(str(config_path), 'w') as f:
                    json.dump(config, f, indent=4)
                
                logging.info(f"Save model at {exp_path}")

        if early_stopping_count == 3:
            logging.info("Early stopping!")
            break

        last_val_loss = val_loss
    
    logging.info(f"End training.{time.time()-start:.2f} sec")

def test(exp_path):
    """학습된 모델을 테스트 셋에 시험해볼 때 사용"""
    # config.json 파일 불러오기
    config = load_config(exp_path)
    torch.manual_seed(config["random_seed"])

    # 데이터셋 불러오기
    dataset_path = Path("./FER-2013/")
    _, test_dataset = load_and_cache_dataset(dataset_path)
    test_dataloader = DataLoader(test_dataset, batch_size=config["batch_size"],
                                 shuffle=True)
    
    # 모델 불러오기
    model = load_fer_model(exp_path)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    # Cross Entropy 손실 함수와 Adam 옵티마이저 사용
    loss_fn = nn.CrossEntropyLoss()
    evaluate(test_dataloader, model, loss_fn)
        
if __name__ == "__main__":
    train(True)