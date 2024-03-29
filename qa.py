from ast import literal_eval

import pandas as pd
from cdqa.pipeline.cdqa_sklearn import QAPipeline
from cdqa.utils.download import download_bnpp_data, download_model
from cdqa.utils.filters import filter_paragraphs


class Ava:
    def __init__(self):
        # princeton_df = pd.read_csv('./data/princeton/articles.csv')
        # princeton_df['paragraphs'] = princeton_df['text'].apply(lambda x: x.splitlines())

        df = pd.read_csv('./data/podcasts/merged_episodes.csv')
        df['paragraphs'] = df['paragraphs'].apply(lambda x: [x])

        self.cdqa_pipeline = self.fit(df) 

        self.df = df

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

        episodeTitle = prediction[1]
        row = self.df.loc[self.df['title'] == episodeTitle].iloc[0]

        print(row)

        return {
            'query': question,
            'answer': prediction[0],
            'title': prediction[1],
            'paragraph': prediction[2],
            'data': row
        }
