import torch
import torch.nn as nn
from torch.autograd import Variable


from math import sqrt

class AdaptiveSoftmax(nn.Module):
    def __init__(self, input_size, cutoff):
        super().__init__()

        self.input_size = input_size
        self.cutoff = cutoff
        self.output_size = cutoff[0] + len(cutoff) - 1

        self.head = nn.Linear(input_size, self.output_size)
        self.tail = nn.ModuleList()

        for i in range(len(cutoff) - 1):
            seq = nn.Sequential(
                nn.Linear(input_size, input_size // 4 ** i, False),
                nn.Linear(input_size // 4 ** i, cutoff[i + 1] - cutoff[i], False)
            )

            self.tail.append(seq)

    def reset(self):
        std = 0.1

        #self.head.weight.data.uniform_(-std, std)
        nn.init.xavier_normal(self.head.weight)

        for tail in self.tail:
            nn.init.xavier_normal(tail[0].weight)
            nn.init.xavier_normal(tail[1].weight)
            #tail[0].weight.data.uniform_(-std, std)
            #tail[1].weight.data.uniform_(-std, std)

    def set_target(self, target):
        self.id = []

        for i in range(len(self.cutoff) - 1):
            mask = target.ge(self.cutoff[i]).mul(target.lt(self.cutoff[i + 1]))

            if mask.sum() > 0:
                self.id.append(Variable(mask.float().nonzero().squeeze(1)))

            else:
                self.id.append(None)

    def forward(self, input):
        output = [self.head(input)]

        for i in range(len(self.id)):
            if self.id[i] is not None:
                output.append(self.tail[i](input.index_select(0, self.id[i])))

            else:
                output.append(None)

        return output

    def log_prob(self, input):
        lsm = nn.LogSoftmax()#.cuda()

        head_out = self.head(input)

        batch_size = head_out.size(0)
        prob = torch.zeros(batch_size, self.cutoff[-1])#.cuda()

        lsm_head = lsm(head_out)
        prob.narrow(1, 0, self.output_size).add_(lsm_head.narrow(1, 0, self.output_size).data)

        for i in range(len(self.tail)):
            pos = self.cutoff[i]
            i_size = self.cutoff[i + 1] - pos
            buffer = lsm_head.narrow(1, self.cutoff[0] + i, 1)
            buffer = buffer.expand(batch_size, i_size)
            lsm_tail = lsm(self.tail[i](input))
            prob.narrow(1, pos, i_size).copy_(buffer.data).add_(lsm_tail.data)

        return prob

class AdaptiveLoss(nn.Module):
    def __init__(self, cutoff):
        super().__init__()

        self.cutoff = cutoff
        self.criterion = nn.CrossEntropyLoss(size_average=False)

    def remap_target(self, target):
        new_target = [target.clone()]

        for i in range(len(self.cutoff) - 1):
            mask = target.ge(self.cutoff[i]).mul(target.lt(self.cutoff[i + 1]))
            new_target[0][mask] = self.cutoff[0] + i

            if mask.sum() > 0:
                new_target.append(target[mask].add(-self.cutoff[i]))

            else:
                new_target.append(None)

        return new_target

    def forward(self, input, target):
        batch_size = input[0].size(0)
        target = self.remap_target(target.data)

        output = 0.0

        for i in range(len(input)):
            if input[i] is not None:
                assert(target[i].min() >= 0 and target[i].max() <= input[i].size(1))
                output += self.criterion(input[i], Variable(target[i]))

        output /= batch_size

        return output



class RNNModel(nn.Module):
    """Container module with an encoder, a recurrent module, and a decoder."""

    def __init__(self, rnn_type, ntoken, ninp, nhid, nlayers, dropout=0.5, tie_weights=False, softmax=True, cutoff=[2000, 10000]):
        super(RNNModel, self).__init__()

        self.drop = nn.Dropout(dropout)
        self.encoder = nn.Embedding(ntoken + 1, ninp)

        if rnn_type in ['LSTM', 'GRU']:
            self.rnn = getattr(nn, rnn_type)(ninp, nhid, nlayers, dropout=dropout)
        else:
            try:
                nonlinearity = {'RNN_TANH': 'tanh', 'RNN_RELU': 'relu'}[rnn_type]
            except KeyError:
                raise ValueError( """An invalid option for `--model` was supplied,
                                 options are ['LSTM', 'GRU', 'RNN_TANH' or 'RNN_RELU']""")
            self.rnn = nn.RNN(ninp, nhid, nlayers, nonlinearity=nonlinearity, dropout=dropout)

        if softmax:
            self.decoder = AdaptiveSoftmax(nhid, [*cutoff, ntoken+1])
        else:
            self.decoder = nn.Linear(nhid, ntoken+1)


        # Optionally tie weights as in:
        # "Using the Output Embedding to Improve Language Models" (Press & Wolf 2016)
        # https://arxiv.org/abs/1608.05859
        # and
        # "Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling" (Inan et al. 2016)
        # https://arxiv.org/abs/1611.01462

        self.adaptive_softmax = softmax
        if tie_weights:
            if nhid != ninp:
                raise ValueError('When using the tied flag, nhid must be equal to emsize')
            self.decoder.weight = self.encoder.weight

        self.init_weights()

        self.rnn_type = rnn_type
        self.nhid = nhid
        self.nlayers = nlayers


    def log_prob(self, input, hidden, target):
        embed = self.encoder(input)
        output, hidden = self.rnn(embed, hidden)
        linear = self.decoder.log_prob(output.contiguous().view(output.size(0) * output.size(1), output.size(2)))

        return linear, hidden


    def init_weights(self):
        initrange = 0.1
        self.encoder.weight.data.uniform_(-initrange, initrange)
        if not self.adaptive_softmax:
            self.decoder.bias.data.fill_(0)
            self.decoder.weight.data.uniform_(-initrange, initrange)

    def forward(self, input, hidden, target=None, training=True):
        emb = self.drop(self.encoder(input))
        output, hidden = self.rnn(emb, hidden)
        output = self.drop(output)

        if self.adaptive_softmax:
            self.decoder.set_target(target.data)

        decoded = self.decoder(output.contiguous().view(output.size(0)*output.size(1), output.size(2)))
        return decoded, hidden

        # decoded = self.decoder(output.view(output.size(0)*output.size(1), output.size(2)))
        # return decoded.view(output.size(0), output.size(1), decoded.size(1)), hidden

    def init_hidden(self, bsz):
        weight = next(self.parameters()).data
        if self.rnn_type == 'LSTM':
            return (Variable(weight.new(self.nlayers, bsz, self.nhid).zero_()),
                    Variable(weight.new(self.nlayers, bsz, self.nhid).zero_()))
        else:
            return Variable(weight.new(self.nlayers, bsz, self.nhid).zero_())
