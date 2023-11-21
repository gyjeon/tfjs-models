# -- coding: utf-8 --
# import 데이터
# origin_text = 데이터.getOriginText()
origin_text = "학점은행제라는 학사학위 프로그램에서 시험을 치는 과정에서 며칠 앞두고 한 학생이 코로나가 심하게 걸렸습니다. 그래서 저는 급히 학생의 상황을 각 학과 교수님들께 말씀을 드리고 원장님과 상의 후 학생이 따로 시험을 칠 수 있도록 해결하였습니다. 이틀 남지 않은 상황으로 처음에는 당황했지만, 교수님들께 사정을 자세히 말씀드려서 시험문제를 다르게 제출하게끔 요청을 드리고 원장님과 이 문제에 대한 것을 어떻게 해결하면 될지 충분히 상의 후 학생에게도 알리고 교수님들께도 말씀을 드렸습니다. 이렇게 일을 하다 보면 예상치 못한 문제로 인해 당황할때가 있습니다. 그럴 때마다 저는 저의 직속 상사와 문제 해결을 충분히 이야기한 후 그 문제를 해결하려고 할 것입니다. 또한 당황스러운 마음을 빨리 진정시키고 상황 문제를 빨리 파악하여 이성적으로 해결하려고 노력할 것입니다."

length_origin_text = len(origin_text)


        

######## 요약하기
    
# https://gongil1st.tistory.com/16
# pip install spaCy
# python -m spacy download en_core_web_sm
# python -m spacy download ko_core_news_sm
# python -m spacy download ko_core_news_md
# python -m spacy download ko_core_news_lg

# 해당 사이트 api
# https://spacy.io/models/ko

# 실제 자소서와 비교
# 다른 라이브러리와 비교가 필요함

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


def spacy_summarize(text, ko_core_news, per):
    nlp = spacy.load(ko_core_news)
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary

if __name__ == '__main__':
    
    print("글자수 : ", length_origin_text)
    print(origin_text)
    
    if length_origin_text < 500:
        per = 0.2
    else:
        per = 0.05
    # arr_ko_core_news = ['ko_core_news_sm','ko_core_news_md','ko_core_news_lg']  #요약결과는 동일한 것 같다.
    arr_ko_core_news = ['ko_core_news_sm'] 
    
    for i in arr_ko_core_news:
        sum_test = spacy_summarize(origin_text, i, per)
        print("--------spacy 요약율 : " , per , " 글자수: ", len(sum_test), "---------")
        
        # import rouge_모델성능평가
        # rouge_v = rouge_모델성능평가.getRouge(sum_test,origin_text)
        # print(rouge_v)
        
        print(sum_test)
    
        