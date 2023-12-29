# MDCN_paddle

MDCN: Multi-scale Dense Cross Network for Image Super-Resolution

[Paper]([MDCN: Multi-Scale Dense Cross Network for Image Super-Resolution | IEEE Journals & Magazine | IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/9208645/))

Paddle 复现版本

## 数据集

分类之后训练集用于训练SR模块
https://aistudio.baidu.com/aistudio/datasetdetail/106261
## aistudio
脚本任务地址: https://aistudio.baidu.com/aistudio/clusterprojectdetail/2356381
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

