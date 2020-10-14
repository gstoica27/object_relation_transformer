import torch
import torch.nn as nn
import torch.nn.functional as F

class myResnet(nn.Module):
    def __init__(self, resnet):
        super(myResnet, self).__init__()
        self.resnet = resnet

    def forward(self, img, att_size=14, precomputed_fc=None):
        x = img.unsqueeze(0)

        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = self.resnet.relu(x)
        x = self.resnet.maxpool(x)

        x = self.resnet.layer1(x)
        x = self.resnet.layer2(x)
        x = self.resnet.layer3(x)
        x = self.resnet.layer4(x)
        if precomputed_fc is not None:
            fc = precomputed_fc
        else:
            fc = x.mean(3).mean(2).squeeze()
        att = F.adaptive_avg_pool2d(x,[att_size,att_size]).squeeze().permute(1, 2, 0)
        # print('FC: {} | Att: {}'.format(fc.shape, att.shape))
        # exit()
        return fc, att

