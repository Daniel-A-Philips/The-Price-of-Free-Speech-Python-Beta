import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import svm
from Twitter import TweepyModule
import datetime

class Correlation:

    def __init__(self,stock,base,handles):
        self.stock = stock
        self.base = base
        self.handles = handles
        self.create_comparison()
        print('Created Correlation.py class')

    def get_tweets(self):
        Tweep = TweepyModule(self.handles,self.start,self.end)
        self.tweet_times = {} # {handle: [tweets in list]
        for handle in self.handles:
            handle_tweet_times = []
            for tweet in Tweep.all_tweets[handle]:
                handle_tweet_times.append((tweet.created_at - datetime.datetime(1970, 1, 1)).total_seconds())
            self.tweet_times[handle] = handle_tweet_times
        self.join_tweet_times = [] # [all tweets in list]
        for handle in self.handles:
            self.join_tweet_times.extend(self.tweet_times[handle])
        self.join_tweet_times.sort(reverse=True)
       # print('join_tweet_times',self.join_tweet_times)
        self.get_closest_tweet_times()
        self.count_times(self.closest_tweet_times)

    def get_closest_tweet_times(self):
        shared_data = self.joint_data_frame.index.values.tolist()
        self.closest_tweet_times = []
        for time in self.join_tweet_times:
            self.closest_tweet_times.append(min(shared_data, key=lambda x:abs(x-time)))

    def count_times(self,data):
        self.num_tweets_time_linked = []
        self.num_tweets_time_linked_dict = {}
        shared_times = self.joint_data_frame.index.values.tolist()
        for time in shared_times:
            self.num_tweets_time_linked_dict[time] = 0
        times_repeated = 1
        times_run = -1
        prev = data[0]
        for time in data:
            times_run += 1
            if times_run == 0: continue
            if time == prev:
                times_repeated += 1
            else:
                self.num_tweets_time_linked.append(times_repeated)
                self.num_tweets_time_linked_dict[time] = times_repeated
                prev = time
                times_repeated = 1

    def chunks(self,list_in, n):
        new_list = []
        temp_list = []
        for i in range(len(list_in)):
            temp_list.append(list_in[i])
            if len(temp_list) % n == 0 and not len(temp_list) == 1:
                new_list.append(temp_list)
                temp_list = []
        return new_list

    def remove_values_from_list(self,the_list, val):
        return [value for value in the_list if value != val]

    def create_joint_data_frame(self, data):
        data = self.remove_values_from_list(data,[])
        self.headers = data[0][1:]
        del data[0]
        self.cols = []
        for line in data: self.cols.append(line[0])
        for i in range(len(data)): del data[i][0]
        self.joint_data_frame = pd.DataFrame(data=data,columns=self.headers,index=self.cols)

    def create_individual_data_frame(self,stock_data,base_data):
        headers = ['Time','Stock Open','Stock High','Stock Low','Stock Close','Stock Volume']
        print(headers)
        stock_data = self.remove_values_from_list(stock_data, [])
        base_data = self.remove_values_from_list(base_data,[])
        del stock_data[0]
        del base_data[0]
        stock_cols = []
        base_cols = []
        for line in stock_data: stock_cols.append(line[0])
        for line in base_data: base_cols.append(line[0])
        self.start = stock_cols[0]
        self.end = stock_cols[-1]
        print('stock_data:',stock_data)
        print('base_data:',base_data)
        self.stock_data_frame = pd.DataFrame(data=stock_data,columns=headers,index=stock_cols)
        self.base_data_frame = pd.DataFrame(data=base_data,columns=headers,index=base_cols)
        self.get_tweets()

    def get_shared_timings(self, stock_data, base_data):
        to_return = [['Time','Stock Open','Stock High','Stock Low','Stock Close','Stock Volume','Base Open','Base High','Base Low','Base Base','Base Volume']]  # ['Time','Stock Open','Stock High','Stock Low','Stock Close','Stock Volume','Base Open','Base High','Base Low','Base Base','Base Volume']
        times_shared = 0
        for stock_row in stock_data:
            line = []
            for base_row in base_data:
                if stock_row[0] == base_row[0]:
                    for data in stock_row:
                        line.append(data)
                    del base_row[0]
                    for data in base_row:
                        line.append(data)
                    times_shared += 1
                    break
            to_return.append(line)
        self.shared_timings = to_return
        return to_return

    def run_model(self):
        self.models_evaluation()

    #https://stackoverflow.com/questions/41925157/logisticregression-unknown-label-type-continuous-using-sklearn-in-python
    def models_evaluation(self):
        classifiers = [
            svm.SVR(),
            linear_model.SGDRegressor(),
            linear_model.BayesianRidge(),
            linear_model.LassoLars(),
            linear_model.ARDRegression(),
            linear_model.PassiveAggressiveRegressor(),
            linear_model.TheilSenRegressor(),
            linear_model.LinearRegression()]
        prediction_length = 10000
        print([ [i,i,i] for i in self.joint_data_frame['# of Tweets'].tolist()])
        trainingData = np.array([ [i,i,i] for i in self.joint_data_frame['# of Tweets'].tolist()]) # Number of Tweets per interval
        trainingScores = np.array([ i for i in self.joint_data_frame['Stock Volume'].tolist()]) # Volume Traded of Stock in interval
        predictionData = np.array([[i,i,i] for i in range(0,prediction_length)])# Array from 0,1000000 of number of stocks

        predicted = classifiers[2].fit(trainingData,trainingScores).predict(predictionData)
        self.SMVI = (sum(predicted) / prediction_length) / len(trainingData)
        print(self.SMVI)

    def add_twitter_data(self):
        print('self.num_tweets_time_linked_dict: ',self.num_tweets_time_linked_dict)
        headers = self.joint_data_frame.columns.values.tolist()
        headers.insert(0,'# of Tweets')
        headers.insert(0,'Time')
        #self.joint_data_frame
        self.data_frame_as_list = [headers]
        times = self.joint_data_frame.index.values.tolist()
        print('Header: ',headers)
        for i in range(0,len(times)):
            print(i)
            line = [self.joint_data_frame.index.values.tolist()[i]] + [self.num_tweets_time_linked_dict[times[i]]] + self.joint_data_frame.values.tolist()[i]
            print('line: ',line)
            self.data_frame_as_list.append(line)



    def create_comparison(self):
        sd_of_stock = self.stock.SDToDisplay
        sd_of_base = self.base.SDToDisplay
        all_stock_data = self.chunks(self.stock.allData['Times'],6)
        all_base_data = self.chunks(self.base.allData['Times'],6)
        self.shared_data = self.get_shared_timings(all_stock_data, all_base_data)
        self.create_joint_data_frame(self.shared_data)
        self.create_individual_data_frame(all_stock_data,all_stock_data)
        print('Running create_joint_data_frame for second time')
        self.add_twitter_data()
        self.create_joint_data_frame(self.data_frame_as_list) #Rerun to use new self.shared_data
        self.run_model()
        print(sd_of_stock,',',sd_of_base)