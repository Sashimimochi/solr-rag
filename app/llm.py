import time
import torch
import streamlit as st
from typing import Optional, List, Any
from langchain.llms import CTranslate2
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema import Generation, LLMResult
from llama_cpp import Llama
from mylogging import logger

torch.cuda.empty_cache()

class Calm2:
    def __init__(self) -> None:
        self.llm = self.load_model()

    @st.cache_resource
    def load_model(_self):
        # ダウンロードしたModelをセット
        model_path = "./model/calm2-7b-chat.Q5_K_M.gguf"
        llm = Llama(model_path=model_path, n_ctx=2048)
        return llm

    def _generate(self, prompt):
        # 生成実行
        streamer = self.llm(
            prompt,
            temperature=0.7,
            top_p=0.3,
            top_k=20,
            repeat_penalty=1.1,
            max_tokens=1024,
            stop=["System:", "User:", "Assistant:"],
            stream=True
        )
        partial_message = ""
        for msg in streamer:
            partial_message += msg.get("choices")[0].get("text")
            yield partial_message

    def generate(self, query):
        prompt = """USER: {query}
Assistant: """.format(query=query)
        output = self._generate(prompt)
        return output

    def generate_with_rag(self, query, context=None):
        prompt = """USER: 貴方はユーザーの質問に答えるAIアシスタントBotです。
ユーザーの質問に対して適切なアドバイスを答えます。
情報として、以下の内容を参考にしてください。
========
{context}
========
さて、「{query}」という質問に対して、上記の情報を元に、答えを考えてみましょう。
ASSISTANT: """.format(context=context, query=query)
        output = self._generate(prompt)
        return output

    def generate_image_caption(self, context):
        prompt = """USER: 以下はとある画像に付けられたキャプションです。
画像の特徴を説明するキーワードが列挙されています。
これを日本語の文章に直してどのような写真であるか解説してください。
========
{context}
========
さて、上記の情報を元にどのような写真か考えてみましょう。
ASSISTANT: """.format(context=context)
        output = self._generate(prompt)
        return output

class Rinna():
    def __init__(self) -> None:
        self.llm = self.load_model()

    @st.cache_resource
    def load_model(_self):
        model_name = "rinna/japanese-gpt-neox-3.6b-instruction-ppo"
        llm = CT2LLM(
            model_path="ct2_model",
            tokenizer_name=model_name,
            device="cuda",
            device_index=[0],
            compute_type="int8",
        )
        return llm

    def generate(self, query):
        inputs = query
        output = self.llm(inputs)
        logger.info(f"出力内容（RAGなし）:\n{output}")
        partial_message = ""
        for out in output:
            time.sleep(0.1)
            partial_message += out
            yield partial_message

    def generate_with_rag(self, query, context):
        template = """ユーザー: 与えられた文脈から、質問に対する答えを抜き出してください。<NL>システム: 分かりました。<NL>ユーザー: 文脈: 赤色のペリレン顔料、Pigment Red 149は、やや青味のある赤色だが他の有機顔料に比べて希釈した色が相対的に黄味に寄る傾向がある。Pigment Red 179は、アントラキノン系の高級顔料であるPigment Red 216よりも、更に暗く強い色調で、より堅牢である。質問: 赤色のペリレン顔料、Pigment Red 149は、やや青味のある赤色だが他の有機顔料に比べて希釈した色が相対的に黄味に寄る傾向がある？<NL>システム: 更に暗く強い色調で、より堅牢である<NL>ユーザー: 文脈: プロレスラーはその考え方をリングの上で表現して観客を楽しませている。しかし、その「受けの美学」が誤解されて「なぜあんな技をよけないのか？」といった批判にもならない的外れなクレームがあることも事実で、それが一般に「真剣勝負」として受け取られない一因にもなっている。こうした「受けの美学」を否定するレスラーも現れ、UWFのようなショー的要素を排除したプロレス（ただし、事前に勝敗は決まっている）が産まれたり、そこからさらに発展して総合格闘技戦に主戦場を移すプロレスラーも多くなっている。質問: ショー的要素を排除したプロレスを行ったのは？<NL>システム: UWFです。<NL>{context}質問: {query}<NL>システム: """
        _context = '''ユーザー: 文脈: {context}'''.format(context=context)
        inputs = template.format(context=_context, query=query)
        output = self.llm(inputs)
        logger.info(f"出力内容（RAGあり）:\n{output}")
        partial_message = ""
        for out in output:
            time.sleep(0.1)
            partial_message += out
            yield partial_message

class CT2LLM(CTranslate2):
    generator_params = {
        "max_length": 256,
        "sampling_topk": 20,
        "sampling_temperature": 0.7,
        "include_prompt_in_result": False,
        "repetition_penalty": 1.5
    }

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        encoded_prompts = self.tokenizer(prompts, add_special_tokens=False)["input_ids"]
        tokenized_prompts = [
            self.tokenizer.convert_ids_to_tokens(encoded_prompt)
            for encoded_prompt in encoded_prompts
        ]

        # 指定したパラメータで文書生成を制御
        results = self.client.generate_batch(tokenized_prompts, **self.generator_params)

        sequences = [result.sequences_ids[0] for result in results]
        decoded_sequences = [self.tokenizer.decode(seq) for seq in sequences]

        generations = []
        for text in decoded_sequences:
            generations.append([Generation(text=text)])

        return LLMResult(generations=generations)
