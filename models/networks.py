import paddle
# import models.archs.classSR_rcan_arch as classSR_rcan_arch
import models.archs.MWCNN as MWCNN
import models.archs.HAN as han
import models.archs.MSRN as MSRN
import models.archs.SRRFN as SRRFN
import models.archs.MLEFGN as MLEFGN
import models.archs.MDCN as MDCN


# Generator
def define_G(opt):
    opt_net = opt['network_G']
    which_model = opt_net['which_model_G']
    # n_resgroups = opt_net["n_resgroups"]
    # n_resblocks = opt_net["n_resblocks"]
    # n_feats = opt_net["n_feats"]
    # reduction = opt_net["reduction"]
    scale = opt_net["scale"]
    # rgb_range = opt_net["rgb_range"]
    # n_colors = opt_net["n_colors"]
    # res_scale= opt_net["res_scale"]
    

    print('*'*100,opt_net)

    # netG = MSRN.MSRN(n_resgroups=n_resgroups,n_resblocks=n_resblocks,n_feats=n_feats,scale = scale,res_scale=res_scale,
    #                    reduction=reduction,rgb_range=rgb_range,n_colors=n_colors)
    # netG = MWCNN.MWCNN(n_resblocks=n_resblocks,n_feats=n_feats)
    # netG = MSRN.MSRN(scale = scale)
    # netG = SRRFN.SRRFN(scale = scale)
    netG = MDCN.MDCN(scale)
    # image restoration
    if which_model == 'MDCN':
        # netG = MWCNN.MWCNN(n_resblocks=n_resblocks,n_feats=n_feats)
        netG = MDCN.MDCN(scale)

    else:
        raise NotImplementedError('Generator model [{:s}] not recognized'.format(which_model))
    

    return netG