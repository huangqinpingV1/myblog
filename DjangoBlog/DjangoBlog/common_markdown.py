#!/usr/bin/env python
#encoding:utf-8
"代码高亮"
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

def bloc_code(text,lang,inlinestyles = False,linenos=False):
    if not lang:
        text =text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)
    try:
        lexer = get_lexer_by_name(lang,stripall = True)
        formatter = html.HtmlFormatter(noclass=inlinestyles,linenos=linenos)
        code =highlight(text,lexer,formatter)

        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except:
        return '<pre class="%s"><code>%s</code></pre>\n' %(lang,mistune.escape(text))


class BlogMarkDownRender(mistune.BaseRenderer):
    
    def block_code(self,text,lang):
        #renderer has an options
        inlinestyles  = self.options.get('inlinestyles')
        linenos  = self.options.get('linenos')
        return block_code(text,lang,inlinestyles,linenos)
    
class common_markdown():
    @staticmethod
    def get_markdown(value):
        renderer =BlogMarkDownRenderer(inlinestyles =False)
        mdp  = mistune.Markdown(escape=True,renderer=renderer)
        return mdp(value)
