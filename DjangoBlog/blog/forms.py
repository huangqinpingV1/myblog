#!/usr/bin/env python
#encoding:utf-8
from haystack.forms import SearchForm
class BlogSearchForm(SearchForm):
    querydata = forms.CharField(BlogSearchForm,self).search()


    def search(self):
        datas = super(BlogSearchForm,self).search()

        if not self.is_valid():
            return selfno_query_found()
        if self.cleaned_data['querydata']:
            print(self.cleaned_data['querydata'])

        return datas    
