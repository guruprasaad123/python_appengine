#!usr/env/python
import json
from pprint import pprint
from google.appengine.api import search
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class data_handler():

    #def ___init__(self):
        #self.analysis_results=[]

    def firebase_init(self):
        self.cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(self.cred,{'databaseURL': 'https://caseletize-demo.firebaseio.com/'});
        return self.cred;

    def Dbreference(self,path):
        # As an admin, the app has access to read and write all data, regradless of Security Rules
        ref = db.reference(path);
        return ref.get();


    def fetch_caselets(self):
        self.firebase_init();
        data = self.Dbreference('ORG-DITIMICS/browse/system/caselets-main-published');
        return data;

    def caselets_doc(self):
        self.items=[];
        caselets = self.fetch_caselets();
        for key,value in caselets.iteritems():
            self.items.append(key);
        return self.items;








    def fetch_json(self):
        with open('analyse.json') as json_data:
            data =json.load(json_data)
            if(data):
                return data;
            else:
                return None;


    def create_doc(self,key,value):
        doc_id=key
        data=value['identifiers']
        fields=[
            search.TextField(name="title",value=data['title']),
            search.TextField(name="details",value=data['name']),
            search.AtomField(name="status",value=data['status']),
            search.AtomField(name="category",value=data['CLS']),
        ]
        document = search.Document(doc_id=doc_id,fields=fields)
        if(document is None):
            return None
        return document



    def modelize(self):
        data = self.fetch_json()
        self.analysis_results=[]
        for X in data:
            document = self.create_doc(X,data[X]);
            result=search.Index(name="ANALYSIS_CASELETS").put(document)
            self.analysis_results.append(result)
        if(self.analysis_results is None):
            return None
        return self.analysis_results
