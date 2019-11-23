from ast import literal_eval

import pandas as pd
from cdqa.pipeline.cdqa_sklearn import QAPipeline
from cdqa.utils.download import download_bnpp_data, download_model
from cdqa.utils.filters import filter_paragraphs


class Ava:
    def __init__(self):
        princeton_df = pd.read_csv('./data/princeton/articles.csv')
        princeton_df['paragraphs'] = princeton_df['text'].apply(lambda x: x.splitlines())
        self.cdqa_pipeline = self.fit(princeton_df) 

        self.df = princeton_df

        print("[Ava] Instance Up")
    
    def fit(self, df):
        # Loading QAPipeline with CPU version of BERT Reader pretrained on SQuAD 1.1
        cdqa_pipeline = QAPipeline(reader='./models/bert_qa.joblib')

        # Fitting the retriever to the list of documents in the dataframe
        cdqa_pipeline.fit_retriever(df=df)

        return cdqa_pipeline

    def ask(self, question):
        print("Received question: %s" % question)

        # Sending a question to the pipeline and getting prediction
        prediction = self.cdqa_pipeline.predict(question)

        # print('query: {}\n'.format(question))
        print('Answer: {}\n'.format(prediction[0]))
        # print('title: {}\n'.format(prediction[1]))
        # print('paragraph: {}\n'.format(prediction[2]))

        return {
            'query': question,
            'answer': prediction[0],
            'title': prediction[1],
            'paragraph': prediction[2]
        }
