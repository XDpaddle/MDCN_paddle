# from model import common
import models.archs.arch_util as common
# import torch
# import torch.nn as nn
import paddle
import paddle.nn as nn

def make_model(args, parent=False):
    return MDCN(args)

class MDCB(nn.Layer):
    def __init__(self, conv=common.default_conv):
        super(MDCB, self).__init__()

        n_feats = 128
        d_feats = 96
        kernel_size_1 = 3
        kernel_size_2 = 5
        act = nn.ReLU(True)

        self.conv_3_1 = conv(n_feats, n_feats, kernel_size_1)
        self.conv_3_2 = conv(d_feats, d_feats, kernel_size_1)
        self.conv_5_1 = conv(n_feats, n_feats, kernel_size_2)
        self.conv_5_2 = conv(d_feats, d_feats, kernel_size_2)
        self.confusion_3 = nn.Conv2D(n_feats * 3, d_feats, 1, padding=0, bias_attr=True)
        self.confusion_5 = nn.Conv2D(n_feats * 3, d_feats, 1, padding=0, bias_attr=True)
        self.confusion_bottle = nn.Conv2D(n_feats * 3 + d_feats * 2, n_feats, 1, padding=0, bias_attr=True)
        self.relu = nn.ReLU()

    def forward(self, x):
        input_1 = x
        output_3_1 = self.relu(self.conv_3_1(input_1))
        output_5_1 = self.relu(self.conv_5_1(input_1))
        input_2 = paddle.concat([input_1, output_3_1, output_5_1], 1)
        input_2_3 = self.confusion_3(input_2)
        input_2_5 = self.confusion_5(input_2)

        output_3_2 = self.relu(self.conv_3_2(input_2_3))
        output_5_2 = self.relu(self.conv_5_2(input_2_5))
        input_3 = paddle.concat([input_1, output_3_1, output_5_1, output_3_2, output_5_2], 1)
        output = self.confusion_bottle(input_3)
        output += x
        return output

class CALayer(nn.Layer):
    def __init__(self, n_feats, reduction=16):
        super(CALayer, self).__init__()
        # global average pooling: feature --> point
        self.avg_pool = nn.AdaptiveAvgPool2D(1)
        # feature channel downscale and upscale --> channel weight
        self.conv_du = nn.Sequential(
                nn.Conv2D(n_feats, n_feats // reduction, 1, padding=0, bias_attr=True),
                nn.ReLU(),
                nn.Conv2D(n_feats // reduction, n_feats, 1, padding=0, bias_attr=True),
                nn.Sigmoid()
        )

    def forward(self, x):
        y = self.avg_pool(x)
        y = self.conv_du(y)
        return x * y

class DB(nn.Layer):
    def __init__(self, conv=common.default_conv):
        super(DB, self).__init__()

        n_feats = 128
        d_feats = 96
        n_blocks = 12

        self.fushion_down = nn.Conv2D(n_feats * (n_blocks - 1), d_feats, 1, padding=0, bias_attr=True)
        self.channel_attention = CALayer(d_feats)
        self.fushion_up = nn.Conv2D(d_feats, n_feats, 1, padding=0, bias_attr=True)

    def forward(self, x):
        x = self.fushion_down(x)
        x = self.channel_attention(x)
        x = self.fushion_up(x)
        return x 
        
class MDCN(nn.Layer):
    def __init__(self, scale,conv=common.default_conv):
        super(MDCN, self).__init__()
        n_feats = 128
        kernel_size = 3
        self.scale_idx = 0
        scale=scale
        act = nn.ReLU()

        n_blocks = 12
        self.n_blocks = n_blocks
        
        # RGB mean for DIV2K
        rgb_range=255
        rgb_mean = (0.4488, 0.4371, 0.4040)
        rgb_std = (1.0, 1.0, 1.0)
        n_colors=3
        self.sub_mean = common.MeanShift(rgb_range, rgb_mean, rgb_std)
        
        # define head module
        modules_head = [conv(n_colors, n_feats, kernel_size)]

        # define body module
        modules_body = nn.LayerList()
        for i in range(n_blocks):
            modules_body.append(MDCB())

        # define distillation module
        modules_dist = nn.LayerList()
        modules_dist.append(DB())

        modules_transform = [conv(n_feats, n_feats, kernel_size)]
        self.upsample = nn.LayerList([
            common.Upsampler(
                conv, s, n_feats, act=True,bias=False
            ) for s in scale
        ])
        # self.upsample = nn.LayerList([
        #     common.Upsampler(
        #         conv, scale, n_feats, act=True
        #     ) 
        # ])
        modules_rebult = [conv(n_feats, n_colors, kernel_size)]

        self.add_mean = common.MeanShift(rgb_range, rgb_mean, rgb_std, 1)

        self.head = nn.Sequential(*modules_head)
        self.body = nn.Sequential(*modules_body)
        self.dist = nn.Sequential(*modules_dist)
        self.transform = nn.Sequential(*modules_transform)
        self.rebult = nn.Sequential(*modules_rebult)

    def forward(self, x):
        x = self.sub_mean(x)
        x = self.head(x)
        front = x

        MDCB_out = []
        for i in range(self.n_blocks):
            x = self.body[i](x)
            if i != (self.n_blocks-1):
                MDCB_out.append(x)

        hierarchical = paddle.concat(MDCB_out,1)
        hierarchical = self.dist(hierarchical)

        mix = front + hierarchical + x

        out = self.transform(mix)
        out = self.upsample[self.scale_idx](out)
        out = self.rebult(out)
        out = self.add_mean(out)
        return out

    def set_scale(self, scale_idx):
        self.scale_idx = scale_idx