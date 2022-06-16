import numpy as np

import chainer
from chainer import cuda, Function, gradient_check, Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

import Model

alines, blines, avocab, av, bvocab, bv, id2wd, extra = np.load("data.npy", allow_pickle=True)

demb = 800
model = Model.ConversationModel(av, bv, avocab, bvocab, demb)
optimizer = optimizers.Adam()
optimizer.setup(model)
#serializers.load_npz('data.model', model)



for epoch in range(3):
    for i in range(len(alines)):
        aln = alines[i]
        alnr = aln[::-1]
        bln = blines[i]
        model.cleargrads()
        loss = model(np.array(alnr), np.array(bln))
        print(float(loss.data))
        loss.backward()
        loss.unchain_backward()
        optimizer.update()
    print(epoch, " epoch finished.")
    serializers.save_npz('data.model', model)


serializers.save_npz('data.model', model)