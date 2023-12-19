import numpy as np
from gensim.models import KeyedVectors
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer
#from mylogger import set_logger, getLogger
#set_logger()
#logger = getLogger(__name__)

model = KeyedVectors.load_word2vec_format(hf_hub_download(repo_id="Word2vec/wikipedia2vec_jawiki_20180420_100d", filename="jawiki_20180420_100d.txt"))
model_name = "line-corporation/line-distilbert-base-japanese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
words = tokenizer.tokenize("もちっとカフェは検索エンジンやそれにまつわる自然言語処理を中心にサークル主である「さしみもち」が興味を持ったことを日々アウトプットしている同人サークルです。Word2VecやSolr関連の書籍の執筆や頒布活動を行っています。")
print(words)

def embedding():
    word_count = 0
    sum_vec = np.zeros(model.vector_size)
    for word in words:
        try:
            sum_vec = model.get_vector(word)
            word_count += 1
        except KeyError:
            pass
    embedding = sum_vec / word_count
    print(embedding)
