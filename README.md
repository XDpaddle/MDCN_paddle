## MDCN_paddle

MDCN: Multi-scale Dense Cross Network for Image Super-Resolution

[Paper]([MDCN: Multi-Scale Dense Cross Network for Image Super-Resolution | IEEE Journals & Magazine | IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/9208645/))

Paddle 复现版本

## 数据集
DIV2K
https://data.vision.ee.ethz.ch/cvl/DIV2K/
Set5
https://drive.google.com/drive/folders/1pRmhEmmY-tPF7uH8DuVthfHoApZWJ1QU


## 训练模型
链接：https://pan.baidu.com/s/1jf0UKI_wf7yRhwdA4AU5Kw 
提取码：u9lr
## 训练步骤
### train sr
```bash
python train.py -opt config/train/train_MDCN.yml
```
## 测试步骤
```bash
python test.py -opt config/test/test_MDCN.yml
```


## 参考资料

- [Xiangtaokong/ClassSR](https://github.com/Xiangtaokong/ClassSR)
- [MIVRC/MDCN-PyTorch](https://github.com/MIVRC/MDCN-PyTorch?tab=readme-ov-file)

