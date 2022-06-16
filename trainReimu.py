import numpy as np

import chainer
from chainer import cuda, Function, gradient_check, Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

import Model

alines, blines, avocab, av, bvocab, bv, id2wd, extra = np.load("data.npy", allow_pickle=True)

demb = 300
model = Model.ConversationModel(av, bv, avocab, bvocab, demb)
optimizer = optimizers.Adam()
optimizer.setup(model)
try:
    serializers.load_npz('reimu.model', model)
except:
    pass

into = []
with open("input_style.txt", "r", encoding="utf-8") as f:
    for line in f:
        into.append(line)

out = []
with open("output_style.txt", "r", encoding="utf-8") as f:
    for line in f:
        out.append(line)
#into = into[0:100]
#out = out[0:100]


for epoch in range(10):
    for i in range(len(into)):
        aln = into[i]
        bln = out[i]
        model.cleargrads()
        loss = model(aln, bln)
        print("{}: {}".format(i, float(loss.data)))
        loss.backward()
        loss.unchain_backward()
        optimizer.update()
        if i % 50 == 0:
            print("保存しました。")
            serializers.save_npz('reimu.model', model)
    print(epoch, " epoch finished.")
    print("保存しました。")
    serializers.save_npz('reimu.model', model)


serializers.save_npz('reimu.model', model)
