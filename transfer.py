# encoding=utf8
import logging
import time
from style import StyleTransfer
from skimage import img_as_ubyte
import caffe
import timeit
import os
from scipy.misc import imsave

class transfer:
    args = None
    content = None
    style  = None
    output = None
    ratio = 1e4
    length = 512
    num_iters = 512
    init = "content"
    model = None
    gpu_id = -1
    verbose = False
    finish_callback = None
    result = None
    def __init__(self,args,finish_callback):
        self.args =args
        self.content = args.get("content")
        self.style = args.get("style")
        self.ratio = args.get("ratio")
        self.model = args.get("model")
        self.gpu_id = args.get("gpu_id")
        self.output = args.get("output")
        self.finish_callback = finish_callback
        pass

    def process(self):
        # logging.info('Transferring...')
        #
        # # set GPU/CPU mode
        # if self.gpu_id == -1:
        #     caffe.set_mode_cpu()
        #     logging.info("Running net on CPU.")
        # else:
        #     caffe.set_device(self.gpu_id)
        #     caffe.set_mode_gpu()
        #     logging.info("Running net on GPU {0}.".format(self.gpu_id))
        #
        # # load images
        # img_style = caffe.io.load_image(self.style)
        # img_content = caffe.io.load_image(self.content)
        # logging.info("Successfully loaded images.")
        #
        # # artistic style class
        # use_pbar = not self.verbose
        # st = StyleTransfer(self.model.lower(), use_pbar=use_pbar)
        # logging.info("Successfully loaded model {0}.".format(self.model))
        #
        # # perform style transfer
        # start = timeit.default_timer()
        # n_iters = st.transfer_style(img_style, img_content, length=self.length,
        #                             init=self.init, ratio=self.ratio,
        #                             n_iter=self.num_iters, verbose=self.verbose)
        # end = timeit.default_timer()
        # logging.info("Ran {0} iterations in {1:.0f}s.".format(n_iters, end - start))
        # img_out = st.get_generated()
        #
        # # output path
        # if self.output is not None:
        #     out_path = self.output
        # else:
        #     out_path_fmt = (os.path.splitext(os.path.split(self.content)[1])[0],
        #                     os.path.splitext(os.path.split(self.style)[1])[0],
        #                     self.model, self.init, self.ratio, self.num_iters)
        #     out_path = "outputs/{0}-{1}-{2}-{3}-{4}-{5}.jpg".format(*out_path_fmt)
        #
        # imsave(out_path, img_as_ubyte(img_out))
        #
        # logging.info('Transfer Done...')
        # self.finish_callback(self.args,out_path)
        self.finish_callback(self.args, "outputs/starry_night.jpg")
        pass