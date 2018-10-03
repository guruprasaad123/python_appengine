#!usr/env/python
import json
from pprint import pprint
from google.appengine.api import search
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from datetime import datetime

class data_handler():

    def ___init__(self):
        self.mapping =       {
      "CAM" : "TEXTFIELD",
      "CAT" : "ATOMFIELD",
      "CLS" : "ATOMFIELD",
      "CUS" : "ATOMFIELD",
      "CUS-CAT" : "ATOMFIELD",
      "CUS-TYP" : "ATOMFIELD",
      "CUS-TYP-CAT" : "ATOMFIELD",
      "TYP-CAT" : "ATOMFIELD",
      "camId" : "ATOMFIELD",
      "createdOn" : "DATEFIELD",
      "desc" : "ATOMFIELD",
      "external-name-header" : "TEXTFIELD",
      "externalname" : "TEXTFIELD",
      "internal-map" : "ATOMFIELD",
      "lastUpdated" : "DATEFIELD",
      "name" : "TEXTFIELD",
      "slug" : "TEXTFIELD",
      "status" : "ATOMFIELD",
      "t" : "TEXTFIELD",
      "title" : "TEXTFIELD",
      "tp" : "TEXTFIELD",
      "type" : "ATOMFIELD",
      "updatedBy" : "ATOMFIELD",
      "updatedOn" : "DATEFIELD",
      "version" : "NUMBERFIELD"
    };
        #identifiers_json = self.fetch_json('identifiersMap.json');
        #self.mapping = json.loads(identifiers_json);
        #self.analysis_results=[]

    def firebase_init(self):
        self.cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(self.cred,{'databaseURL': 'https://caseletize-demo.firebaseio.com/'});
        return self.cred;

    def Dbreference(self,path):
        # As an admin, the app has access to read and write all data, regradless of Security Rules
        ref = db.reference(path);
        return ref.get();

    def get_field(self,key,value):
        try:
            if(self.mapping[key]):
                if(self.mapping[key]=='TEXTFIELD'):
                    return search.TextField(name=key,value=value);
                elif(self.mapping[key]=='ATOMFIELD'):
                    return search.AtomField(name=key,value=value);
                elif(self.mapping[key]=='NUMBERFIELD'):
                    return search.NumberField(name=key,value=value);
                elif(self.mapping[key]=='HTMLFIELD'):
                    return search.HtmlField(name=key,value=value);
                elif(self.mapping[key]=='DATEFIELD'):
                    timestamp=value;
                    timestamp = timestamp if timestamp>0 else -timestamp;
                    value=datetime.fromtimestamp(timestamp/1000.0);
                    return search.DateField(name=key,value=value);
                elif(self.mapping[key]=='GEOFIELD'):
                    return search.GeoField(name=key,value=value);
                else:
                    return None;
            else:
                return None;
        except KeyError,keyError:
            print(keyError);
            return None;

    def create_caselet_docs(self,identifiers,key):
        doc_id=key;
        fields=[];
        for key , value in identifiers.iteritems():
            field = self.get_field(key,value);
            if(field is None):
                continue;
            else:
                fields.append(field);
        document=search.Document(doc_id=doc_id,fields=fields);
        if(document is None):
            return None;
        else:
            return document;

    def fetch_caselets(self):
        #self.firebase_init();
        #data = self.Dbreference('ORG-DITIMICS/browse/system/caselets-main-published');
        self.caselet_index = [];
        self.mapping =  {
      "CAM" : "TEXTFIELD",
      "CAT" : "HTMLFIELD",
      "CLS" : "HTMLFIELD",
      "CUS" : "HTMLFIELD",
      "camId" : "HTMLFIELD",
      "createdOn" : "DATEFIELD",
      "desc" : "HTMLFIELD",
      "lastUpdated" : "DATEFIELD",
      "name" : "TEXTFIELD",
      "slug" : "TEXTFIELD",
      "status" : "HTMLFIELD",
      "t" : "TEXTFIELD",
      "title" : "TEXTFIELD",
      "tp" : "TEXTFIELD",
      "type" : "HTMLFIELD",
      "updatedBy" : "HTMLFIELD",
      "updatedOn" : "DATEFIELD",
      "version" : "NUMBERFIELD"
    };

        caselets = self.fetch_json('caselets.json');
        #identifiers_json = self.fetch_json('identifiersMap.json');
        #self.mapping = json.loads(identifiers_json);

        for key,value in caselets.iteritems():
            identifiers = value['identifiers'];
            document = self.create_caselet_docs(identifiers,key);
            result = search.Index(name="CASELETS_SEARCH").put(document);
            self.caselet_index.append(result);

        return self.caselet_index;

    def caselets_doc(self):
        self.items=[];
        caselets = self.fetch_json('caselets.json');
        for key,value in caselets.iteritems():
            self.items.append(key);
        print('items ', self.items);
        return self.items;

    def fetch_json(self,file_name):
        with open(file_name) as json_data:
            data =json.load(json_data)
            if(data):
                return data;
            else:
                return None;

    def fetch_analyse(self):
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
        data = self.fetch_analyse()
        self.analysis_results=[]
        for X in data:
            document = self.create_doc(X,data[X]);
            result=search.Index(name="ANALYSIS_CASELETS").put(document)
            self.analysis_results.append(result)
        if(self.analysis_results is None):
            return None
        return self.analysis_results
