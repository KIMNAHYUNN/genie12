import os
import json
import time
import logging
import datetime

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision.io import read_image

from model import MiniXception

emotions = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
positive_emotions = ["happy", "neutral", "surprise"]

NUM_CLASSES = 7

class FER13(Dataset):
    """Dataset object for https://www.kaggle.com/msambare/fer2013"""
    def __init__(self, path):
        self.images = []
        self.labels = []
        for label, emotion in enumerate(emotions):
            emotion_dir = os.path.join(path, emotion)
            for file_name in os.listdir(emotion_dir):
                file_path = os.path.join(emotion_dir, file_name)
                img_tensor = transform(read_image(file_path))
                self.images.append(img_tensor)
                self.labels.append(label)

    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]
    
    def __len__(self):
        return len(self.labels)

def transform(img_tensor):
    """Return image tensor normalized to -1 from 1"""
    return torch.Tensor((img_tensor/255.0 - 0.5)*2) 

def load_fer_model(model_path):
    model = MiniXception(NUM_CLASSES)
    model.load_state_dict(torch.load(model_path))
    # model.eval() TODO: 왜 eval 넣으면 성능 떨어지는지 
    return model

def inference(model, image):
    """Return emotion, probability of the emotion and is_positive_emotino(boolean).
    
    Input is (48, 48) gray numpy tensor.
    """
    transformed = transform(image)
    transformed = transformed.view(1, 1, 48, 48)
    
    result = model(transformed)

    result = result.squeeze() # (1, C) => (C,)
    emotion_idx = result.argmax().item()
    emotion = emotions[emotion_idx]

    probs = {emotion:prob for emotion, prob in zip(emotions, result.tolist())}   
    prob = probs[emotion]
    
    is_pos_emotion = emotion in positive_emotions
    return emotion, prob, is_pos_emotion

def evaluate(dataloader, model, loss_fn):
    """Return validation loss and accuracy of the model"""
    #model.eval()
    total = len(dataloader.dataset)
    num_batches = len(dataloader)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    total_loss = 0
    correct = 0
    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device)
            labels = labels.to(device)
            pred = model(images)

            total_loss += loss_fn(pred, labels).item()
            correct += (pred.argmax(1) == labels).type(torch.float).sum().item()

    val_loss = total_loss / num_batches
    acc = correct / total
    logging.info(f"Val loss: {val_loss:>8f} Acc: {(100*acc):>0.1f}%")
    return val_loss, acc

def train(save_model):
    config = {
        "batch_size": 64,
        "learning_rate":  1e-3,
        "weight_decay": 0.01,
        "max_epochs": 200,
        "random_seed": 42,
    }
    torch.manual_seed(config["random_seed"])
    logging.info("Start loading datasest.")
    start = time.time()
    train_data_path = "./dataset/train"
    test_data_path = "./dataset/test"
    train_dataset = FER13(train_data_path)
    test_dataset = FER13(test_data_path)
    logging.info(f"End loading dataset. {time.time()-start:.2f} sec")

    train_dataloader = DataLoader(train_dataset, batch_size=config["batch_size"],
                                  shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=config["batch_size"],
                                 shuffle=True)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MiniXception(NUM_CLASSES)   
    model.to(device)
    
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config["learning_rate"],     
                                 weight_decay=config["weight_decay"])
    logging.info("Start training.")
    start = time.time()
    early_stop_count = 0
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
            optimizer.zero_grad() #?
            loss.backward()
            optimizer.step()

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
            if save_model:
                if exp_path is not None:
                    os.remove(model_path)
                    os.remove(config_path)
                    os.rmdir(exp_path)
                now = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                exp_path = f"./models/{now}-{saved_acc:.4f}"
                os.makedirs(exp_path, exist_ok=True)

                model_path = os.path.join(exp_path, "model.pt")
                torch.save(saved_params, model_path)

                config_path = os.path.join(exp_path, "config.json")
                with open(str(config_path), 'w') as f:
                    json.dump(config, f, indent=4)

                logging.info(f"Save model at {exp_path}")

        if early_stopping_count == 3:
            logging.info("Early stopping!")
            break

        last_val_loss = val_loss
    


    logging.info(f"End training.{time.time()-start:.2f} sec")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    train(True)
