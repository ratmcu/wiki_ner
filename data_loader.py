import os
import tarfile
import pandas as pd
# !pip install wget
import wget
import pickle
import ast
import random
class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
        
class WikiNameEntities():
    def __init__(self, path = './', sampling = 'random'):
#         download the files or check them
#         read all the files and load
        self.path_prefix =  path
        data_dir = self.path_prefix + '/data'    
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        if os.path.isfile(data_dir + '/' + 'dataset.tar.gz'):
            print('data set is inplace')
        else:            
            print('downloading the dataset from the git')
            wget.download('https://github.com/ratmcu/wiki_ner/blob/master/dataset.tar.gz?raw=true', out  = data_dir)
        tar = tarfile.open(data_dir + '/' + 'dataset.tar.gz', mode='r')
        tar.extractall(data_dir)
        tar.close()

        if os.path.isfile(data_dir + '/' + 'president_list.pkl'):
            print('url list is inplace')
        else:
            print('downloading the url list from the git')
            wget.download('https://github.com/ratmcu/wiki_ner/blob/master/president_list.pkl?raw=true', out  = data_dir)
            
        self.annotation_index = 0
        self.page_index = 0
        self.dictionary = {'sentences': [], 'annotations': [] } 
        self.total_annotations = 0
         
        self.chain_files() # will read each file and chain them into the bigger dictionary
        self.index_list  = list(0 for i in range(0, self.total_annotations))
        self.sampling_method = ''
        self.sampling_methods = {'random', 'none'}
        self.set_sampling_method('random')
                                
    def set_sampling_method(self, method):
        if method in self.sampling_methods:
            self.sampling_method =  method
        else:
            print('sampling method is invalid')
            raise RuntimeError

    def load_file(self, country, name):
        anntn_pth = self.path_prefix + '/data' + '/dataset' + '/politicians' + '/' + country + '/' + name + '/' + 'annotations.csv'
        sntnce_pth = self.path_prefix + '/data'+ '/dataset' + '/politicians' + '/' + country + '/' + name + '/' + 'sentences.csv'
        if os.path.isfile(anntn_pth) and os.path.isfile(sntnce_pth):
            annotation_df = pd.read_csv(anntn_pth)
            annotations = []
            for i in range(0, len(annotation_df)):
                annotations.append(ast.literal_eval(annotation_df.iloc[i][0]))
            sentences = pd.read_csv(sntnce_pth)
            return [annotations, sentences]
        return None
    
    def chain_files(self):
        pages = 0
        with open(self.path_prefix + '/data' + '/' + 'president_list.pkl', 'rb') as f:
            prsdnt_list = pickle.load(f)
        for country in prsdnt_list:
            for president in country['presidents']:
                if country['country'] and president['name']:
                    contents = self.load_file(country['country'], president['name'])
                    if contents:
                        self.total_annotations = self.total_annotations + len(contents[0])
#                         annotation = contents[0]
#                         sentences = contents[1]
                        for i in range(0, len(contents[0])):
                            self.dictionary['annotations'].append({'page'      : pages, 
                                                                   'annotation': contents[0][i]}) #each annotation is a dict of (page #, annotation) 
                        pages = pages + 1
                        self.dictionary['sentences'].append(contents[1])
        print('loaded {0} pages with {1} annotations'.format(pages, self.total_annotations))
    
    def random_fill_index_list(self):
        check_list = list(0 for i in range(0, self.total_annotations)) #list to keep track of the indices to be sampled
        self.index_list = list(0 for i in range(0, self.total_annotations)) #list to keep track of the indices to be sampled                
        fill_count = 0                                                      #number of indices filled to be drawn
        while fill_count != self.total_annotations:                    #
            index = random.randrange(0, self.total_annotations)        #draw a random index    
            if check_list[index] == 0:                                      #draw is fresh
                check_list[index] = 1
                self.index_list[fill_count] = index
                fill_count = fill_count + 1
                                
    def non_random_fill_index_list(self):
        check_list = list(0 for i in range(0, self.total_annotations)) #list to keep track of the indices to be sampled
        fill_count = 0                                                      #number of indices filled to be drawn
        while fill_count != self.total_annotations:                    #
            if check_list[fill_count] == 0:                                      #draw is fresh
                check_list[fill_count] = 1
                self.index_list[fill_count] = fill_count
                fill_count = fill_count + 1
                                
    def __iter__(self):
        self.annotation_index = 0
        self.page_index = 0
        self.index_list  = list(0 for i in range(0, self.total_annotations-1))
        if self.sampling_method == 'random':                                
            self.random_fill_index_list()  
        elif self.iteration_sampling == 'none':
            self.non_random_fill_index_list()
        else:
            self.random_fill_index_list()
        return self
    
    def __next__(self):
        if self.annotation_index == self.total_annotations:
            raise StopIteration
        annotation = self.dictionary['annotations'][self.index_list[self.annotation_index]]
        sentence = self.dictionary['sentences'][annotation['page']].iloc[annotation['annotation'][0]][0] # annotation['annotation'][0] is the sentence number, 1 is the char poitions and the 2 is the category
        self.annotation_index += 1
        return sentence, annotation['annotation']     
#         return annotation