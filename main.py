import re
import random

############################################################
# Markov Models
############################################################

def tokenize(text):
    punctuations = "&,'!($#@*^%-:"
    return re.findall(r"[\w]+|["+punctuations+"]",text)
    #pass

def ngrams(n, tokens):
    start = '<START>'
    ini = []
    fin = []
    tokens.append('<END>')
    if (n==1):
        for i in range(len(tokens)):
            list_t = []
            list_t.append(tuple([]))
            list_t.append(tokens[i])
            fin.append(tuple(list_t))
    else:
        for entry in range(n-1):
            ini.append(start)
        for i in range(len(tokens)):
            list_t = []
            list_t.append(tuple(ini))
            list_t.append(tokens[i])
            ini.remove(ini[0])
            ini.append(tokens[i])
            fin.append(tuple(list_t))
    return(fin)
    #pass

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.internal_cnt = []
        #pass

    def update(self, sentence):
        tokens = tokenize(sentence)
        self.internal_cnt.extend(ngrams(self.n, tokens))
        #pass

    def prob(self, context, token):
        context_token_cnt = 0
        context_cnt = 0
        for entry in (self.internal_cnt):
            if context == entry[0]:
                context_cnt = context_cnt + 1
            if tuple([context, token]) == entry:
                context_token_cnt = context_token_cnt + 1
        probability = (context_token_cnt)/(context_cnt)
        return probability
        #pass
 
    def random_token(self, context):
        Token = []
        rand = random.random() # hint as given in instructions
        for entry in self.internal_cnt:
            if entry[0] == context:
                Token.append(entry[1])
        Token.sort()
        length = len(Token)
        if length != 0:
            if int(rand*length) >= length:
                return Token[length - 1]
            return Token[int(rand*length)]
        else:
            return ' '
        #pass
  
    def random_text(self, token_count):
        t = ' '
        list_t = []
        for i in range(token_count):
            if t == "<END>":
                context = ()
                for j in range(self.n-1):
                    context += ("<START>",)
            else:
                context = self.update_context(list_t)
            t = self.random_token(context)
            list_t.append(t)
        text = ' '.join(list_t)
        return text
        #pass

    def update_context(self,list_t):
        context = ()
        for temp in reversed(range(self.n-1)):
            if len(list_t) < temp + 1:
                context = context + ("<START>",)
            else:
                context = context + (list_t[len(list_t)-1-temp],)
        return context


    def perplexity(self, sentence):
        t = tokenize(sentence)
        ngms = ngrams(self.n,t)
        per = 1.0
        for entry in ngms:
            cntxt = entry[0]
            tkn = entry[1]
            per = per * (1.0/self.prob(cntxt,tkn))
        per = per**(1./len(ngms))
        return per
        #pass

def create_ngram_model(n, path):
    model = NgramModel(n)
    text_file = open(path)
    for sentence in text_file:
        model.update(sentence)
    return model
    #pass

#Verifying the code:

#m = NgramModel(1)
#m.update("a b c d")
#m.update("a b a b")
#print(m.prob((), "a"))
#print(m.prob((), "c"))
#print(m.prob((), "<END>"))
#
#m = NgramModel(2)
#m.update("a b c d")
#m.update("a b a b")
#print(m.prob(("<START>",), "a"))
#print(m.prob(("b",), "c"))
#print(m.prob(("a",), "x"))
#
#m = NgramModel(1)
#m.update("a b c d")
#m.update("a b a b")
#random.seed(1)
#print([m.random_token(()) for i in range(25)])
#
#m = NgramModel(2)
#m.update("a b c d")
#m.update("a b a b")
#random.seed(2)
#print([m.random_token(("<START>",)) for i in range(6)])
#print([m.random_token(("b",)) for i in range(6)])
#
#m = NgramModel(1)
#m.update("a b c d")
#m.update("a b a b")
#random.seed(1)
#print(m.random_text(13))
#
#m = NgramModel(2)
#m.update("a b c d")
#m.update("a b a b")
#random.seed(2)
#print(m.random_text(15))
#
#m = create_ngram_model(1, "frankenstein.txt")
#print(m.random_text(15))
#m = create_ngram_model(2, "frankenstein.txt")
#print(m.random_text(15))
#m = create_ngram_model(3, "frankenstein.txt")
#print(m.random_text(15))
#m = create_ngram_model(4, "frankenstein.txt")
#print(m.random_text(15))
#
#print(ngrams(1, ["a", "b", "c"]))
#print(ngrams(2, ["a", "b", "c"]))
#print(ngrams(3, ["a", "b", "c"]))
#
#print(tokenize("'Medium-rare,' she said."))
#print(tokenize("  This is an example.  "))
#
#m = NgramModel(1)
#m.update("a b c d")
#m.update("a b a b")
#print(m.perplexity("a b"))
#
#m = NgramModel(2)
#m.update("a b c d")
#m.update("a b a b")
#print(m.perplexity("a b"))
