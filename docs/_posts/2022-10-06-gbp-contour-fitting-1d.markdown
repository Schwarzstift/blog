---
author: Chris Carstensen
layout: post
title:  "Gaussian Belief Propagation - 1D Contour Fitting"
date:   2022-10-06 20:45:08 +0200
categories: GBP
---

# TL;DR
This blog builds on top of a [prior blog post](https://schwarzstift.github.io/blog/gbp/2022/10/04/gaussian-belief-propagation.html) of mine, where I explained a Gaussian Belief Propagation (GBP) implementation.
Here I want to replicate the Contour Fitting application presented in [this blog](https://gaussianbp.github.io/).
Despite the fact, that it is well described in the mentioned blog article, I like to see the formulars and code side by side.

So that's what this blog post is about: 
1. Reimplementing the Contour Fitting application
2. Set it side by side with the equations from the mentioned blog post.

If that's of interest to you, go ahead an read further.
The complete sources can be found [here](https://github.com/Schwarzstift/blog/tree/gh-pages/src/GaussianBeliefPropagation/internal)

# Problem description

Here we want to estimate the contour from multiple measurements.
For this, we have a fixed number of variable nodes, which represents a part of the estimated contour.

The Factor Graph proposed by [this blog](https://gaussianbp.github.io/) looks something like this:


    
![png](data:image/png;base64,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lh3/GPPEiRO57LLLALjuuusc+YvkhHe3/ROA3gMGexxJy6LN95o1a/j0Kqtjx46lvLyc+++/nzvvvJOMjLhb+zFJ1nxPnz79uH+PGTOGzMxMrr/+evbu3XvCV2a3JGu+GxUXF7N8+XKWLl3K9ddf71g83bt3N8XFxS0+zBDJlW5mdnZ2Qovu0qVL+fe//82MGTNOaB/46etMo5rqKva8u5PsnFy6n9HL63BaFG2+T7as9Wc/+1mqq6v55JOYJsqPWzLn+2QaH0Cqra1NTJCtaA/5njlzJt/5znc4++yzHY2nQ4cOBshsaZtIrnTTMzMzHat8gwYNwhjD22+/TUNDA/v37+euu+6iY8eOLFy40KnDJNT729+mIRikZ78Bvp+424l8v/LKK3Tq1ImuXbsmONqTaw/5DgaD1NXVsW3bNhYsWMCkSZPo2bOne4F/SrLn+ze/+Q0lJSU888wzjn9zzsjICAAtfh2MpOjWVldXO3YXJTc3l969e7Nr1y7effdd7r77bo4ePcrixYtpK48Yv/t2qH/Ue8CgE97buuE1/rD8p+zevo3ammq6nPYZLvnGdMZ/9etuhwnEn++33nqLRx55hPnz55OS4s20G+0h3507dz528+ziiy9m1apVboV8gmTO9+HDh5k7dy5LliwhJyfH8XhqamoagJqWtomk6FZXVlbGvnrlSQwZMoRdu3axatUqHn74Yfr06cOsWbOcPERC7Qr3u3r1P/6k3LH5LX787a/zpW98iykzZtLQYHl32z9x6iZkrGLNd2lpKZdffjkjRozw7EYatI98r1+/nsrKSoqLi7nzzjuZOHEiL7zwgid/6JI537feeitnnXUW11xzTUJiqaiosEB1S9tEkq0De/fudbzoPvXUUyxYsICGhgYWL15Menq6k4dIqPcarwSanJSv/Olp+n52ON+ce9ux1z57/hg3QzupWPJ9+PBhvvjFL5Kdnc3q1asTPsaxJe0h30OHDgVg1KhRDBs2jOHDh/P000/zla98xYWIj5es+d62bRvLly/nhRde4NChQ0Bo2Fjjf48ePUpubm5csXz00UcWONDSNpH0arfs2LEj28mhFY3N72AwyLhx446NTmgL6mpr+KDkHTKysjitd5/j3svIymL739/kD8v/h30f7vEowhNFm+/q6momTZrEvn37eO655zx9cqo95LupoUOHEggEKCkpSUR4LUrmfO/cuZP6+nrGjh1Lfn4++fn5x4aTjR07lvPPP/lDIZGqr69nx44d2cCWlrZr9UrXWnu4Y8eOB7Zv3x73E2mNLrvssoieqPKj93dsp76ujt79B5/w1e+Km+YQrA/yp1+vYNW9d3H2kGFcPfu/GDTycx5FGxJNvuvr67nyyiv55z//ycsvv8wZZ5yR4Ohaluz5Ppk33niDhoYGevfu7WBUkUnmfI8ePZp169Yd99qWLVuYPXs2y5cvZ9iwYXHF8a9//YusrKwDtbW1R1raLqJmTEpKyqZNmzZd6sXTYJWVlTz77LMAvP/++xw5coQnn3wSgPPOO8/1ovB/4xdPzEVmdjbX/dd8rr3ldnZsfpOVd97KPbOm8auNb/ty6NvJzJw5kzVr1nDPPfdQWVnJhg0bjr3Xv39/8vJafNjGccme7wkTJnDRRRcxYMAAMjMz2bJlC4sWLWLw4MFMnjzZ9XiSOd8FBQWMGTPmpO81tnTisWnTJlJSUlodDhFR0T148ODLGzdu/MK1117r+sj4ffv2nfB0TuO/H3nkEa677jpX4xn/tW8w/mvfaHEbYwz9zh3BqIsn8uSD9/p+2M2nrV27FoB58+ad8N66deuaPWkTJdnzPWLECH7729/y3nvvAdCzZ09uuOEG5syZ48l9jmTPdyJt3Lix5uDBgy+3tl2ktx03rl27ttZam+F2gnv27NkmWhEP3jaXQEoKAwtH0bFTAe++vZWnfn4fF199XZs6KXfv3u11CBFJlnwvXLiwTYxPT5Z8NzVmzBhH6ou1lueff74W2NjatpEW3df27dtXsXHjxtyRI0fGF12SOv3Ms3jtz6t5/c+rqa+rpfsZvbj2lvlc9JWrvA4tKSnf7lK+W7Zhwwb27dtXDrze2rYRTe0IkJqa+v3LL7/8jscff7zNLNmTiKkd/SDSqR29oJy7S/n2hyuvvLLyqaeeur2+vn5Ja9tG3P0OBoOPrF69OnDgQItD0ERE2pX9+/ezZs2aQDAYjGjxuIiLrrX24/T09D+uXLkyGHt4IiLJZeXKlcH09PT/tdZGNCNUVOM8jhw5suiee+6pOXjwYGzRiYgkkYMHD7Jo0aKaI0eOLIp0n6iKrrV2U11d3aqZM2dWRR+eiEhyuemmm6pqa2sftdb+PdJ9oh7RXF5ePnv16tVHnnnmmWh3FRFJGmvWrGHNmjWHKyoqZkezX9RF11pbXlFR8bVvfvOblWoziEh7dPDgQa677rrKioqKq6y1FdHsG9Oze9ba9bW1tatmzJhR1ZaGdYiIxMtay4wZM6pqamoetdauj3b/mB+YLi8v/8/nn3++ZM6cObUqvAK0qXGVIrEIrzJc+/zzz5dE21ZoFHPRtdZWHD16dMzKlSv3zJ8/v85vv3B+i8dpfvv5rLXMnz+/zus4EsmPOU9mfvv5Gs/xhx56aM/Ro0fHRNtWaBTxE2kiIhI//8/HJiKSRFR0RURcpKIrIuIiFV0RERep6IqIuOj/AytaCBScrlORAAAAAElFTkSuQmCC
)
    


Here the x position of the variable nodes $$v_n$$ are fixed. 
In my example, they are uniformly distributed in an interval from $$[0,1]$$.
This reduces the complexity of this problem to only one dimension.
In other words, whats left is to estimate the correct height of each variable node.

But first things first, let's create the variable nodes using this function: 




<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.output_html .hll { background-color: #ffffcc }
.output_html { background: #f8f8f8; }
.output_html .c { color: #3D7B7B; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #9C6500 } /* Comment.Preproc */
.output_html .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.output_html .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #E40000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #008400 } /* Generic.Inserted */
.output_html .go { color: #717171 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #687822 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #717171; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #767600 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #A45A77 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">generate_variable_nodes</span><span class="p">(</span><span class="n">num_variable_nodes</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span> <span class="n">dims</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">VariableNode</span><span class="p">]:</span>
    <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    Generates variable nodes with an x pos uniform over the interval [0,1]</span>
<span class="sd">    :param num_variable_nodes: number of nodes to generate</span>
<span class="sd">    :param dims: dimensions for each node</span>
<span class="sd">    :return: list containing all generated nodes</span>
<span class="sd">    &quot;&quot;&quot;</span>
    <span class="n">nodes</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">num_variable_nodes</span><span class="p">):</span>
        <span class="n">node</span> <span class="o">=</span> <span class="n">VariableNode</span><span class="p">(</span><span class="n">dims</span><span class="p">)</span>
        <span class="n">node</span><span class="o">.</span><span class="n">x_pos</span> <span class="o">=</span> <span class="n">i</span> <span class="o">/</span> <span class="p">(</span><span class="n">num_variable_nodes</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span>
        <span class="n">nodes</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">node</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">nodes</span>
</pre></div>




Having our variable nodes, we need our measurements.
Let's start with a simple step. which is sampled from using this function:




<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.output_html .hll { background-color: #ffffcc }
.output_html { background: #f8f8f8; }
.output_html .c { color: #3D7B7B; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #9C6500 } /* Comment.Preproc */
.output_html .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.output_html .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #E40000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #008400 } /* Generic.Inserted */
.output_html .go { color: #717171 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #687822 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #717171; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #767600 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #A45A77 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">generate_measurement_step</span><span class="p">():</span>
    <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    Samples measuremetns from a step function</span>
<span class="sd">    :return: measurement (x,y)</span>
<span class="sd">    &quot;&quot;&quot;</span>
    <span class="n">height_measurement</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">random</span><span class="p">()</span> <span class="o">*</span> <span class="mf">0.</span>
    <span class="n">x_pos</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">random</span><span class="p">()</span>
    <span class="k">if</span> <span class="n">x_pos</span> <span class="o">&lt;</span> <span class="mf">0.5</span><span class="p">:</span>
        <span class="n">height_measurement</span> <span class="o">+=</span> <span class="mf">0.5</span>
    <span class="k">return</span> <span class="n">x_pos</span><span class="p">,</span> <span class="n">height_measurement</span>
</pre></div>




With this sampling function, we can now generate actual measurements and the according measurement factors (depicted red in the image above).
The general idea is that the measurement is represented as a factor.
This factor is connected to two variable nodes, which are left and right from the measurement.

Apart from the measurement itself, the measurement factor needs also the measurement function and the corresponding jaccobian.
both are functions, which are described in more detail below.




<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.output_html .hll { background-color: #ffffcc }
.output_html { background: #f8f8f8; }
.output_html .c { color: #3D7B7B; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #9C6500 } /* Comment.Preproc */
.output_html .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.output_html .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #E40000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #008400 } /* Generic.Inserted */
.output_html .go { color: #717171 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #687822 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #717171; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #767600 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #A45A77 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">generate_measurement_factors</span><span class="p">(</span><span class="n">v_nodes</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">VariableNode</span><span class="p">],</span> <span class="n">measurement_generator</span><span class="p">,</span>
                                 <span class="n">num_measurements</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span> <span class="n">meas_noise</span><span class="p">,</span> <span class="n">use_huber</span><span class="p">:</span> <span class="nb">bool</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Tuple</span><span class="p">[</span>
    <span class="n">List</span><span class="p">[</span><span class="n">FactorNode</span><span class="p">],</span> <span class="n">List</span><span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">]]:</span>
    <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    Generates the measurement factors and measurements (one factor for each measurement)</span>
<span class="sd">    :param v_nodes: all variable nodes</span>
<span class="sd">    :param measurement_generator:  measurement generating function</span>
<span class="sd">    :param num_measurements: number of measurements to generate</span>
<span class="sd">    :param meas_noise: measurement noise</span>
<span class="sd">    :return: list of all measurement factors</span>
<span class="sd">    &quot;&quot;&quot;</span>
    <span class="n">f_nodes</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">gen_meas</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">num_measurements</span><span class="p">):</span>
        <span class="n">measurement_x_pos</span><span class="p">,</span> <span class="n">height_measurement</span> <span class="o">=</span> <span class="n">measurement_generator</span><span class="p">()</span>
        <span class="n">idx_var_node</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">measurement_x_pos</span> <span class="o">*</span> <span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">v_nodes</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span><span class="p">))</span>

        <span class="n">adj_vars</span> <span class="o">=</span> <span class="p">[</span><span class="n">v_nodes</span><span class="p">[</span><span class="n">idx_var_node</span><span class="p">],</span> <span class="n">v_nodes</span><span class="p">[</span><span class="n">idx_var_node</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]]</span>
        <span class="n">meas_fn</span> <span class="o">=</span> <span class="n">measurement_fn</span>
        <span class="n">jac_fn</span> <span class="o">=</span> <span class="n">measurement_fn_jac</span>
        <span class="n">f_nodes</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">FactorNode</span><span class="p">(</span><span class="n">adj_vars</span><span class="p">,</span> <span class="n">meas_fn</span><span class="p">,</span> <span class="n">meas_noise</span><span class="p">,</span> <span class="n">height_measurement</span><span class="p">,</span> <span class="n">jac_fn</span><span class="p">,</span> <span class="n">use_huber</span><span class="p">,</span>
                                  <span class="p">[</span><span class="n">v_nodes</span><span class="p">[</span><span class="n">idx_var_node</span><span class="p">]</span><span class="o">.</span><span class="n">x_pos</span><span class="p">,</span> <span class="n">v_nodes</span><span class="p">[</span><span class="n">idx_var_node</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span><span class="o">.</span><span class="n">x_pos</span><span class="p">,</span> <span class="n">measurement_x_pos</span><span class="p">]))</span>
        <span class="n">gen_meas</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([</span><span class="n">measurement_x_pos</span><span class="p">,</span> <span class="n">height_measurement</span><span class="p">]))</span>

    <span class="k">return</span> <span class="n">f_nodes</span><span class="p">,</span> <span class="n">gen_meas</span>
</pre></div>




Below is the measurement function and it's jaccobian defined.

The basic idea is to split the measurement between the two adjacent nodes according to the x position of the measurement and the nodes.




<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.output_html .hll { background-color: #ffffcc }
.output_html { background: #f8f8f8; }
.output_html .c { color: #3D7B7B; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #9C6500 } /* Comment.Preproc */
.output_html .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.output_html .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #E40000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #008400 } /* Generic.Inserted */
.output_html .go { color: #717171 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #687822 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #717171; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #767600 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #A45A77 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">measurement_fn</span><span class="p">(</span><span class="n">means</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">],</span> <span class="n">x_pos_i</span><span class="p">:</span> <span class="nb">float</span><span class="p">,</span> <span class="n">x_pos_j</span><span class="p">:</span> <span class="nb">float</span><span class="p">,</span> <span class="n">x_pos_of_measurement</span><span class="p">:</span> <span class="nb">float</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">:</span>
    <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    Simple measurement function which divides the measurement between two factors</span>
<span class="sd">    :param means: current height estimate of the nodes</span>
<span class="sd">    :param x_pos_i: x position of the left variable</span>
<span class="sd">    :param x_pos_j: x position of the right variable</span>
<span class="sd">    :param x_pos_of_measurement: x position of the measurement</span>
<span class="sd">    :return: measurement</span>
<span class="sd">    &quot;&quot;&quot;</span>
    <span class="n">x_m</span> <span class="o">=</span> <span class="n">x_pos_of_measurement</span>
    <span class="n">x_i</span> <span class="o">=</span> <span class="n">x_pos_i</span>
    <span class="n">x_j</span> <span class="o">=</span> <span class="n">x_pos_j</span>
    <span class="n">y_i</span> <span class="o">=</span> <span class="n">means</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
    <span class="n">y_j</span> <span class="o">=</span> <span class="n">means</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span>
    <span class="n">lam</span> <span class="o">=</span> <span class="p">(</span><span class="n">x_m</span> <span class="o">-</span> <span class="n">x_i</span><span class="p">)</span> <span class="o">/</span> <span class="p">(</span><span class="n">x_j</span> <span class="o">-</span> <span class="n">x_i</span><span class="p">)</span>
    <span class="k">return</span> <span class="p">(</span><span class="mi">1</span> <span class="o">-</span> <span class="n">lam</span><span class="p">)</span> <span class="o">*</span> <span class="n">y_i</span> <span class="o">+</span> <span class="n">lam</span> <span class="o">*</span> <span class="n">y_j</span>
</pre></div>







<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.output_html .hll { background-color: #ffffcc }
.output_html { background: #f8f8f8; }
.output_html .c { color: #3D7B7B; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #9C6500 } /* Comment.Preproc */
.output_html .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.output_html .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #E40000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #008400 } /* Generic.Inserted */
.output_html .go { color: #717171 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #687822 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #717171; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #767600 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #A45A77 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">measurement_fn_jac</span><span class="p">(</span><span class="n">means</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">],</span> <span class="n">x_pos_i</span><span class="p">:</span> <span class="nb">float</span><span class="p">,</span> <span class="n">x_pos_j</span><span class="p">:</span> <span class="nb">float</span><span class="p">,</span>
                       <span class="n">x_pos_of_measurement</span><span class="p">:</span> <span class="nb">float</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">:</span>
    <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    Jacobian of the measurement function above</span>
<span class="sd">    :param means: current height estimate of the nodes</span>
<span class="sd">    :param x_pos_i: x position of the left variable</span>
<span class="sd">    :param x_pos_j: x position of the right variable</span>
<span class="sd">    :param x_pos_of_measurement: x position of the measurement</span>
<span class="sd">    :return: Jacobian</span>
<span class="sd">    &quot;&quot;&quot;</span>
    <span class="n">x_m</span> <span class="o">=</span> <span class="n">x_pos_of_measurement</span>
    <span class="n">x_i</span> <span class="o">=</span> <span class="n">x_pos_i</span>
    <span class="n">x_j</span> <span class="o">=</span> <span class="n">x_pos_j</span>
    <span class="n">gamma</span> <span class="o">=</span> <span class="p">(</span><span class="n">x_m</span> <span class="o">-</span> <span class="n">x_i</span><span class="p">)</span> <span class="o">/</span> <span class="p">(</span><span class="n">x_j</span> <span class="o">-</span> <span class="n">x_i</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([[(</span><span class="mi">1</span> <span class="o">-</span> <span class="n">gamma</span><span class="p">),</span> <span class="n">gamma</span><span class="p">]])</span>
</pre></div>




Next to the measurement factors, we need smoothing factors as well, which are depicted blue in the image above.
These smoothing factors - as the name implies - tries to smooth the surface of the resulting contour.

This time there is no direct measurement, which is why I set it to 0.
The measurement function now calculates the difference between the y-values, which is basically to be minimized.




<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.output_html .hll { background-color: #ffffcc }
.output_html { background: #f8f8f8; }
.output_html .c { color: #3D7B7B; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #9C6500 } /* Comment.Preproc */
.output_html .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.output_html .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #E40000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #008400 } /* Generic.Inserted */
.output_html .go { color: #717171 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #687822 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #717171; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #767600 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #A45A77 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">generate_smoothing_factors</span><span class="p">(</span><span class="n">v_nodes</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">VariableNode</span><span class="p">],</span> <span class="n">meas_noise</span><span class="p">,</span> <span class="n">use_huber</span><span class="p">:</span> <span class="nb">bool</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">FactorNode</span><span class="p">]:</span>
    <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    Generate factor nodes with the above defined smoothing measurement function</span>
<span class="sd">    :param v_nodes: all variable nodes</span>
<span class="sd">    :param meas_noise: measurement noise</span>
<span class="sd">    :return: list of all smoothing factor nodes</span>
<span class="sd">    &quot;&quot;&quot;</span>
    <span class="n">f_nodes</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">v_nodes</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span><span class="p">):</span>
        <span class="n">adj_vars</span> <span class="o">=</span> <span class="p">[</span><span class="n">v_nodes</span><span class="p">[</span><span class="n">i</span><span class="p">],</span> <span class="n">v_nodes</span><span class="p">[</span><span class="n">i</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]]</span>
        <span class="n">meas_fn</span> <span class="o">=</span> <span class="n">smoothing</span>
        <span class="n">measurement</span> <span class="o">=</span> <span class="mf">0.</span>
        <span class="n">jac_fn</span> <span class="o">=</span> <span class="n">smoothing_jac</span>
        <span class="n">f_nodes</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">FactorNode</span><span class="p">(</span><span class="n">adj_vars</span><span class="p">,</span> <span class="n">meas_fn</span><span class="p">,</span> <span class="n">meas_noise</span><span class="p">,</span> <span class="n">measurement</span><span class="p">,</span> <span class="n">jac_fn</span><span class="p">,</span> <span class="n">use_huber</span><span class="p">,</span> <span class="p">[]))</span>
    <span class="k">return</span> <span class="n">f_nodes</span>
</pre></div>







<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.output_html .hll { background-color: #ffffcc }
.output_html { background: #f8f8f8; }
.output_html .c { color: #3D7B7B; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #9C6500 } /* Comment.Preproc */
.output_html .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.output_html .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #E40000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #008400 } /* Generic.Inserted */
.output_html .go { color: #717171 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #687822 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #717171; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #767600 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #A45A77 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">smoothing</span><span class="p">(</span><span class="n">means</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">])</span> <span class="o">-&gt;</span> <span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">:</span>
    <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    Measurement function of the smoothing factor node</span>
<span class="sd">    Simple smoothing function, forcing the nodes to hold similar height values</span>
<span class="sd">    :param means: height estimates for each adjacent nodes (to the factor</span>
<span class="sd">    &quot;&quot;&quot;</span>
    <span class="k">return</span> <span class="n">means</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">-</span> <span class="n">means</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span>
</pre></div>







<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.output_html .hll { background-color: #ffffcc }
.output_html { background: #f8f8f8; }
.output_html .c { color: #3D7B7B; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #9C6500 } /* Comment.Preproc */
.output_html .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.output_html .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #E40000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #008400 } /* Generic.Inserted */
.output_html .go { color: #717171 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #687822 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #717171; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #767600 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #A45A77 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">smoothing_jac</span><span class="p">(</span><span class="n">linearization_point</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">])</span> <span class="o">-&gt;</span> <span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">:</span>
    <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    Jacobian of the smoothing function</span>
<span class="sd">    :param linearization_point: point of evaluation (not used as linear)</span>
<span class="sd">    &quot;&quot;&quot;</span>
    <span class="k">return</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([[</span><span class="mi">1</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">]])</span>
</pre></div>




Lastly, we need to fit everything together in a little "main" function as shown below:




<style>pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.output_html .hll { background-color: #ffffcc }
.output_html { background: #f8f8f8; }
.output_html .c { color: #3D7B7B; font-style: italic } /* Comment */
.output_html .err { border: 1px solid #FF0000 } /* Error */
.output_html .k { color: #008000; font-weight: bold } /* Keyword */
.output_html .o { color: #666666 } /* Operator */
.output_html .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.output_html .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.output_html .cp { color: #9C6500 } /* Comment.Preproc */
.output_html .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.output_html .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.output_html .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.output_html .gd { color: #A00000 } /* Generic.Deleted */
.output_html .ge { font-style: italic } /* Generic.Emph */
.output_html .gr { color: #E40000 } /* Generic.Error */
.output_html .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.output_html .gi { color: #008400 } /* Generic.Inserted */
.output_html .go { color: #717171 } /* Generic.Output */
.output_html .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.output_html .gs { font-weight: bold } /* Generic.Strong */
.output_html .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.output_html .gt { color: #0044DD } /* Generic.Traceback */
.output_html .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.output_html .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.output_html .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.output_html .kp { color: #008000 } /* Keyword.Pseudo */
.output_html .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.output_html .kt { color: #B00040 } /* Keyword.Type */
.output_html .m { color: #666666 } /* Literal.Number */
.output_html .s { color: #BA2121 } /* Literal.String */
.output_html .na { color: #687822 } /* Name.Attribute */
.output_html .nb { color: #008000 } /* Name.Builtin */
.output_html .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.output_html .no { color: #880000 } /* Name.Constant */
.output_html .nd { color: #AA22FF } /* Name.Decorator */
.output_html .ni { color: #717171; font-weight: bold } /* Name.Entity */
.output_html .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.output_html .nf { color: #0000FF } /* Name.Function */
.output_html .nl { color: #767600 } /* Name.Label */
.output_html .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.output_html .nt { color: #008000; font-weight: bold } /* Name.Tag */
.output_html .nv { color: #19177C } /* Name.Variable */
.output_html .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.output_html .w { color: #bbbbbb } /* Text.Whitespace */
.output_html .mb { color: #666666 } /* Literal.Number.Bin */
.output_html .mf { color: #666666 } /* Literal.Number.Float */
.output_html .mh { color: #666666 } /* Literal.Number.Hex */
.output_html .mi { color: #666666 } /* Literal.Number.Integer */
.output_html .mo { color: #666666 } /* Literal.Number.Oct */
.output_html .sa { color: #BA2121 } /* Literal.String.Affix */
.output_html .sb { color: #BA2121 } /* Literal.String.Backtick */
.output_html .sc { color: #BA2121 } /* Literal.String.Char */
.output_html .dl { color: #BA2121 } /* Literal.String.Delimiter */
.output_html .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.output_html .s2 { color: #BA2121 } /* Literal.String.Double */
.output_html .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.output_html .sh { color: #BA2121 } /* Literal.String.Heredoc */
.output_html .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.output_html .sx { color: #008000 } /* Literal.String.Other */
.output_html .sr { color: #A45A77 } /* Literal.String.Regex */
.output_html .s1 { color: #BA2121 } /* Literal.String.Single */
.output_html .ss { color: #19177C } /* Literal.String.Symbol */
.output_html .bp { color: #008000 } /* Name.Builtin.Pseudo */
.output_html .fm { color: #0000FF } /* Name.Function.Magic */
.output_html .vc { color: #19177C } /* Name.Variable.Class */
.output_html .vg { color: #19177C } /* Name.Variable.Global */
.output_html .vi { color: #19177C } /* Name.Variable.Instance */
.output_html .vm { color: #19177C } /* Name.Variable.Magic */
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">main</span><span class="p">():</span>
    <span class="n">use_huber</span> <span class="o">=</span> <span class="kc">True</span>
    <span class="n">num_var</span> <span class="o">=</span> <span class="mi">20</span>
    <span class="n">num_measurements</span> <span class="o">=</span> <span class="mi">10</span>
    <span class="n">noise</span> <span class="o">=</span> <span class="mf">0.01</span>
    <span class="n">meas_noise</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([[</span><span class="n">noise</span><span class="p">]])</span>
    <span class="n">smooth_noise</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([[</span><span class="n">noise</span><span class="p">]])</span>
    <span class="n">variable_nodes</span> <span class="o">=</span> <span class="n">generate_variable_nodes</span><span class="p">(</span><span class="n">num_var</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
    <span class="n">factor_nodes</span><span class="p">,</span> <span class="n">measurements</span> <span class="o">=</span> <span class="n">generate_measurement_factors</span><span class="p">(</span><span class="n">variable_nodes</span><span class="p">,</span> <span class="n">generate_measurement_step</span><span class="p">,</span>
                                                              <span class="n">num_measurements</span><span class="p">,</span> <span class="n">meas_noise</span><span class="p">,</span> <span class="n">use_huber</span><span class="p">)</span>
    <span class="n">factor_nodes</span><span class="o">.</span><span class="n">extend</span><span class="p">(</span><span class="n">generate_smoothing_factors</span><span class="p">(</span><span class="n">variable_nodes</span><span class="p">,</span> <span class="n">smooth_noise</span><span class="p">,</span> <span class="n">use_huber</span><span class="p">))</span>

    <span class="n">factor_graph</span> <span class="o">=</span> <span class="n">FactorGraph</span><span class="p">(</span><span class="n">variable_nodes</span><span class="p">,</span> <span class="n">factor_nodes</span><span class="p">)</span>

    <span class="n">num_iters</span> <span class="o">=</span> <span class="mi">30</span>
    <span class="n">viz</span> <span class="o">=</span> <span class="n">ContourFittingViz</span><span class="p">(</span><span class="n">variable_nodes</span><span class="p">,</span> <span class="n">measurements</span><span class="p">,</span> <span class="n">num_iters</span><span class="p">)</span>

    <span class="k">for</span> <span class="nb">iter</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">num_iters</span><span class="p">):</span>
        <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;iteration: &quot;</span> <span class="o">+</span> <span class="nb">str</span><span class="p">(</span><span class="nb">iter</span><span class="p">))</span>
        <span class="n">factor_graph</span><span class="o">.</span><span class="n">synchronous_iteration</span><span class="p">()</span>
        <span class="n">viz</span><span class="o">.</span><span class="n">add_iteration</span><span class="p">(</span><span class="n">variable_nodes</span><span class="p">)</span>

    <span class="n">viz</span><span class="o">.</span><span class="n">render</span><span class="p">()</span>
</pre></div>




Here ContourFittingViz is just a little util class to plot the results.
An example can be seen below, which is also the endresult of this blog entry.
![alt text](LineFitting.png "Title")
