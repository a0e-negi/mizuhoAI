import numpy as np
import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L
 
class ConversationModel(chainer.Chain):
    avocab = {}
    bvocab = {}
 
    def __init__(self, av, bv, avo, bvo, k):
        super(ConversationModel, self).__init__(
            embedx = L.EmbedID(av, k),
            embedy = L.EmbedID(bv, k),
            H = L.LSTM(k, k),
            H2 = L.LSTM(k*2, k),
            A = L.Linear(k*2, k),
            A2 = L.Linear(k, k),
            W = L.Linear(k, k),
            W2 = L.Linear(k, k),
            W3 = L.Linear(k, k),
            W4 = L.Linear(k, k),
            W5 = L.Linear(k*4, bv),
        )
        self.avocab = avo
        self.bvocab = bvo
        self.k = k
 
    def __call__(self, aline, bline):
        att = []
        for i in range(len(aline)):
            try:
                wid = self.avocab[aline[i]]
            except:
                wid = self.avocab[" "]
            x_k = F.relu(self.embedx(Variable(np.array([wid], dtype=np.int32))))
            h = F.relu(self.H(x_k))
            att.append(h.data[0])
        x_k = F.relu(self.embedx(Variable(np.array([self.avocab['<eos>']], dtype=np.int32))))
        try:
            tx = Variable(np.array([self.bvocab[bline[0]]], dtype=np.int32))
        except:
            tx = Variable(np.array([self.bvocab[" "]], dtype=np.int32))
        h = F.relu(self.H(x_k))
        att.append(h.data[0])
        w = F.relu(self.W(h))
        w2 = F.relu(self.W2(h))
        w3 = F.relu(self.W3(h))
        w4 = F.relu(self.W4(h))
        accum_loss = F.softmax_cross_entropy(self.W5(
            Variable(np.array([chainer.functions.concat([w.data[0], w2.data[0], w3.data[0], w4.data[0]], axis=0).data], dtype=np.float32))
        ), tx)
        for i in range(len(bline)):
            try:
                wid = self.bvocab[bline[i]]
            except:
                wid = self.bvocab[" "]
            x_k = F.relu(self.embedy(Variable(np.array([wid], dtype=np.int32))))
            try:
                next_wid = self.bvocab['<eos>']  if (i == len(bline) - 1) else self.bvocab[bline[i+1]]
            except:
                next_wid = self.bvocab['<eos>']  if (i == len(bline) - 1) else self.bvocab[" "]
            tx = Variable(np.array([next_wid], dtype=np.int32))

            i = 0
            c = [[0]*self.k]
            for at in att:
                a = F.tanh(self.A(Variable(np.array([chainer.functions.concat([h.data[0], at], axis=0).data], dtype=np.float32))))
                a2 = F.softmax(self.A2(a))
                c += a2.data
            c = np.array(c, dtype=np.float32)
            
            h = F.relu(self.H2(Variable(np.array([chainer.functions.concat([x_k.data[0], c[0]], axis=0).data], dtype=np.float32))))
            w = F.relu(self.W(h))
            w2 = F.relu(self.W2(h))
            w3 = F.relu(self.W3(h))
            w4 = F.relu(self.W4(h))
            loss = F.softmax_cross_entropy(self.W5(
                Variable(np.array([chainer.functions.concat([w.data[0], w2.data[0], w3.data[0], w4.data[0]], axis=0).data], dtype=np.float32))
            ), tx)
            accum_loss += loss
        return accum_loss
