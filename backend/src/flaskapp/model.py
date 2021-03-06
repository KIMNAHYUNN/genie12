#############################################################
#############################################################

### model.py: 프로젝트에서 사용한 딥러닝 모델 클래스를 구현

#############################################################
#############################################################

import torch
import torch.nn as nn

class MiniXception(nn.Module):
    """PyTorch implementation of https://github.com/oarriaga/face_classification"""
    """감정 분류에 사용한 딥러닝 모델"""

    def __init__(self, num_classes, eps, momentum):
        """딥러닝 모델의 구조 정의"""
        super(MiniXception, self).__init__()
        self.num_classes = num_classes

        # (64, 64) resizing 생략
        # Input: (1, 48, 48)
        # out channel - 단순화를 위해 4로 지정 (default: 5)
        self.start_layers = nn.Sequential(
            nn.Conv2d(1, 4, 3, bias=False), # (4, 46, 46)
            nn.BatchNorm2d(4, eps, momentum),
            nn.ReLU(),
            nn.Conv2d(4, 4, 3, bias=False), # (4, 44, 44)
            nn.BatchNorm2d(4, eps, momentum),
            nn.ReLU()
        )

        # 신경망 가운데에 위치한 4개의 블록
        self.blocks = nn.ModuleList([Block(in_channels, None, eps, momentum) for in_channels in [4, 8, 16, 32]])

        self.conv = nn.Conv2d(64, self.num_classes, 3, padding="same")
        # Global Average Pooling - 경량화
        self.gap = nn.AdaptiveAvgPool2d((1,1)) # (감정 개수, 1, 1)
        self.softmax = nn.Softmax(dim = 1) # (감정 개수, 1, 1)

    def forward(self, x):
        """
        입력 데이터를 __init__에서 만든 레이어들에 차례차례 통과
        """
        x = self.start_layers(x)    # 딥러닝 모델에 입력된 데이터

        for block in self.blocks:
            x = block(x)
        
        x = self.conv(x)
        x = self.gap(x)
        x = x.view(-1, x.shape[1]) # (감정 개수, 1, 1) => (감정 개수,)
        return self.softmax(x)

class DepthWiseSepConv(nn.Module):
    """Depth-wise Seperable Convolution (경량화)"""
    def __init__(self, in_channels, out_channels, kernel_size):
        super(DepthWiseSepConv, self).__init__()
        self.depthwise = nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size,
                                   padding="same", groups=in_channels, bias=False)
        self.pointwise = nn.Conv2d(out_channels, out_channels, kernel_size=1)
    
    def forward(self, x):
        x = self.depthwise(x)
        return self.pointwise(x)

class Block(nn.Module): # 4회 반복 구조
    def __init__(self, in_channels, out_channels=None, eps=1e-5, momentum=0.1):
        super(Block, self).__init__()
        self.in_channels = in_channels
        self.out_channels = 2*in_channels if out_channels is None else out_channels

        # Residual
        self.conv_res = nn.Conv2d(self.in_channels, self.out_channels, kernel_size=1,
                                  stride=2, padding=0, bias=False)
        self.bnorm_res = nn.BatchNorm2d(self.out_channels, eps, momentum)
        
        self.dws_conv_1 = DepthWiseSepConv(self.in_channels, self.out_channels, 3)
        self.bnorm_1 = nn.BatchNorm2d(self.out_channels, eps, momentum)
        self.act_1 = nn.ReLU()
        self.dws_conv_2 = DepthWiseSepConv(self.out_channels, self.out_channels, 3)
        self.bnorm_2 = nn.BatchNorm2d(self.out_channels, eps, momentum)
        self.pool = nn.MaxPool2d(3, stride=2, padding=1)

    def forward(self, x):
        res = self.conv_res(x)
        res = self.bnorm_res(res)
        
        x = self.dws_conv_1(x)
        x = self.bnorm_1(x)
        x = self.act_1(x)
        x = self.dws_conv_2(x)
        x = self.bnorm_2(x)
        x = self.pool(x)
        
        return x + res

# for test
class CNN(nn.Module):
    def __init__(self, num_classes):
        super(CNN, self).__init__()
        self.blocks = nn.Sequential(
            CNNBlock(1, 16, 7),
            CNNBlock(16, 32, 5),
            CNNBlock(32, 64, 3),
            CNNBlock(64, 128, 3)
        )

        self.classifier = nn.Sequential(
            nn.Conv2d(128, 256, 3, padding="same"),
            nn.BatchNorm2d(256),
            nn.Conv2d(256, num_classes, 3, padding="same"),
            nn.AdaptiveAvgPool2d((1,1)), # Global average pooling
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        x = self.blocks(x)
        return self.classifier(x).squeeze()

# for test 
class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size):
        super(CNNBlock, self).__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, padding="same"),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.AvgPool2d(2, padding=1),
            nn.Dropout(0.5)
        )

    def forward(self, x):
        return self.block(x)
   
# file end