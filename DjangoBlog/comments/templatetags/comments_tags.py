#!/usr/bin/env python
# encoding: utf-8

from django import template
from django.template.loader import render_to_string
#引用当前包下的model Comment类
from ..models import Comment
#引用其他模块或应用的Article类
from blog.models import Article

register = template.Library()
"""
@register.simple_tag(name='get_comment_count')
def GetCommentCount(parser,token):
    #查询对应文章的评论总数
    commentcount = Comment.objects.filter(article__author_id=token).count();
    return "0" if commentcount == 0 else str(commentcount)+ "  comments"
@register.inclusion_tag('comments/tag/post_comment.html')
def load_post_comment(article):
    return  {'article':article}
""" 
@register.simple_tag
def parse_commenttree(commentlist,comment):
    print("parse_commenttree() 递归查找")
    datas = []
    def parse(c):
        childs = commentlist.filter(parent_comment = c)
        for child in childs:
            datas.append(child)
            parse(child)
    parse(comment)
    return datas

@register.inclusion_tag('comments/tags/comment_item.html')
def show_comment_item(comment,ischild):
    depth = 1 if ischild else 2
    return  {'comment_item':comment,'depth':depth}
