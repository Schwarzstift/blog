---
author: Chris Carstensen
layout: post
title:  "Gaussian Belief Propagation - An Implementation guide"
date:   2022-10-04 18:01:08 +0200
categories: GBP
---

# TL;DR
This blog post is just me trying to reproduce the results of the excellent blog post: [A visual introduction to Gaussian Belief Propagation](https://gaussianbp.github.io/).
Please check this site out if you want to have a general introduction.
Additional resources about Belief Propagation in general can be found in the references \[2,3\].
The complete code can be found [here](https://github.com/Schwarzstift/blog/tree/gh-pages/src/GaussianBeliefPropagation/internal)

# Disclaimer 
In here I want to focus on the implementational details of the basic algorithm.
Applications will be described in a second blog post.
This implementation does NOT focus on performance. 
Instead it focus on code readability so that it is easier to understand what's going on.
The main purpose I'm doing this, is to learn for myself. As reading stuff and actually replicating it, is something different.
To give credit where it belongs: I got some ideas on how to implement this from [this repository](https://github.com/joeaortiz/gbp) and from the original [source code](https://github.com/gaussianBP/gaussianBP.github.io/tree/2f724b9f59447ae58101c3c8d8f4b4ec32eb82a2/src) of the blog post.

Elaborates a bit more on the code. Nevertheless, you can find the complete implementation in my [repository](https://github.com/Schwarzstift/blog/tree/gh-pages/src/GaussianBeliefPropagation/internal).
If thats of interest to you, go ahead and read more :)

Without further ado, lets dive right into this.

## What is needed?

Before I start implementing stuff, I like to step back and look at the bigger picture.
What do we need for a basic GBP algorithm to work?

Gaussian Belief Propagation runs on a model called [Factor Graphs](https://en.wikipedia.org/wiki/Factor_graph) as such depited in the figure below, which basically defines our data structure.

In such a Factor Graph, factor nodes are depicted as rectangles.
Red factor nodes represent arbitraty factos, which have to be modeled according to your application.
The blue factor nodes represent the priors of the variable nodes, which are depicted as circles.
Not every variable node has to have a prior factor.
Two variable nodes can be connected via multiple factor nodes. 



    
![png](data:image/png;base64,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
)
    



Hence we need the following classes:
- a *gaussian state* class containing
    - mean and variance or eta and lambda in canonical form
- a *variable node* class containing
    - the current state belief of the node
    - a function to update the belief
    - a function to compute the message from a node to a factor
- a *factor node* class containing
    - the factor of the factor node
    - a function to compute the message from a factor to a node
- a *factor graph* class
    - which wraps everything up

Having this in mind, we can start implementing the base classes of a Gaussian Belief Propagation algorithm.

## Gaussian State

As the name Gaussian Belief Propagation implies is the bases of all the Gaussian distribution.
Hence we start with implementing a tiny helper class to keep the mean vector and covariance matrix close together.
As pointed out in this [blog post](https://gaussianbp.github.io/), the canonical form offers some computational advantages above the moments form.
Hence we will also use the state in this form.




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
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">class</span> <span class="nc">GaussianState</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">dimensionality</span><span class="p">:</span> <span class="nb">int</span><span class="p">):</span>
        <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">        Initialize a gaussian state</span>
<span class="sd">        :param dimensionality: number of dimensions of the state</span>
<span class="sd">        :param eta: canonical form of mean</span>
<span class="sd">        :param lam: canonical form of the covariance matrix</span>
<span class="sd">        &quot;&quot;&quot;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">dim</span> <span class="o">=</span> <span class="n">dimensionality</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">eta</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">dim</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">lam</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">dim</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">dim</span><span class="p">])</span>
</pre></div>




## Variable Node 

The variable node represent the random variables in your factor graph.
As we use Gaussian Belief Propagation (GBP), each variable is assumed to be normal distributed.

Keep in mind, that a variable node can represent a single random variable as well as a vector of random variables.
In this implementation, the number of random variables in refered to as the *dimension* of the VariableNode.





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
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">class</span> <span class="nc">VariableNode</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">dimensions</span><span class="p">:</span> <span class="nb">int</span><span class="p">):</span>
        <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">        Initialize the belief and prior with gaussian states</span>
<span class="sd">        :param dimensions: the dimensions of the gaussian state</span>
<span class="sd">        &quot;&quot;&quot;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">idx</span> <span class="o">=</span> <span class="n">VariableNode</span><span class="o">.</span><span class="n">idx_counter</span>
        <span class="n">VariableNode</span><span class="o">.</span><span class="n">idx_counter</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">belief</span> <span class="o">=</span> <span class="n">GaussianState</span><span class="p">(</span><span class="n">dimensions</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">prior</span> <span class="o">=</span> <span class="n">GaussianState</span><span class="p">(</span><span class="n">dimensions</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">dimensions</span> <span class="o">=</span> <span class="n">dimensions</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">adj_factors_idx</span> <span class="o">=</span> <span class="p">[]</span>  <span class="c1"># will be filled by Factors on creation</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">factor_nodes</span> <span class="o">=</span> <span class="p">[]</span>  <span class="c1"># will be filled at the end by the FactorGraph</span>

        <span class="bp">self</span><span class="o">.</span><span class="n">mu</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">dimensions</span><span class="p">)</span>  <span class="c1"># for debug/output purpose</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">sigma</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">([</span><span class="n">dimensions</span><span class="p">,</span> <span class="n">dimensions</span><span class="p">])</span>  <span class="c1"># for debug/output purpose</span>
</pre></div>




The prior and belief of the Variable node are initialized with zero vectors and matrixes. Indicating an uninitialized variable with no prior.
One can define the prior afterwards, which is effectively the same as adding another factor node, which is only connected to this variable node and serves as it's prior.


### Belief update

Here I want to cite the Appendix B from [here](https://gaussianbp.github.io/):
> To compute the belief at a variable node, you take the product of incoming messages from all adjacent factors: 
> $$b_i(x_i)= \prod_{s \in N(i)} m_{f_s \rightarrow x_i}, $$
> where N(i) denotes the neighbours of nodes i. A Gaussian message has the canonical form: 
> $$ m = N^{-1}(x,\eta,\Lambda) \propto exp(-\frac{1}{2} x^\intercal \Lambda x+\eta^\intercal x), $$
> and so taking products of these messages is equivalent to summing the respective information vectors and precision matrices. The belief parameters $$\eta_{b_i}$$ and $$\Lambda_{b_i}$$ are therefore:
> $$ \eta_{b_i} = \sum_{s \in N(i)} \eta_{f_s \rightarrow x_i} \text{ and }  \Lambda_{b_i} = \sum_{s \in N(i)} \Lambda_{f_s \rightarrow x_i}$$
$$ N(i) = \text{set of adjacent nodes of i} $$

As the last two equations suggest, the belief update is simply a sum over the incoming messages.

So let's implement this:




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
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">class</span> <span class="nc">VariableNode</span>
    <span class="o">...</span>

    <span class="k">def</span> <span class="nf">update_belief</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">        Updates the belief of a variable node &amp; sends a message to all adjacent factors</span>
<span class="sd">        &quot;&quot;&quot;</span>
        <span class="n">eta</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">prior</span><span class="o">.</span><span class="n">eta</span><span class="o">.</span><span class="n">copy</span><span class="p">()</span>
        <span class="n">lam</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">prior</span><span class="o">.</span><span class="n">lam</span><span class="o">.</span><span class="n">copy</span><span class="p">()</span>
        <span class="k">for</span> <span class="n">factor_idx</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">adj_factors_idx</span><span class="p">:</span>
            <span class="n">factor</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_nodes</span><span class="p">[</span><span class="n">factor_idx</span><span class="p">]</span>
            <span class="n">eta_message</span><span class="p">,</span> <span class="n">lam_message</span> <span class="o">=</span> <span class="n">factor</span><span class="o">.</span><span class="n">get_message_for</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">idx</span><span class="p">)</span>
            <span class="n">eta</span> <span class="o">+=</span> <span class="n">eta_message</span>
            <span class="n">lam</span> <span class="o">+=</span> <span class="n">lam_message</span>

        <span class="bp">self</span><span class="o">.</span><span class="n">belief</span><span class="o">.</span><span class="n">eta</span> <span class="o">=</span> <span class="n">eta</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">belief</span><span class="o">.</span><span class="n">lam</span> <span class="o">=</span> <span class="n">lam</span>
        <span class="k">if</span> <span class="n">np</span><span class="o">.</span><span class="n">linalg</span><span class="o">.</span><span class="n">det</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">belief</span><span class="o">.</span><span class="n">lam</span><span class="p">)</span> <span class="o">!=</span> <span class="mi">0</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">sigma</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">linalg</span><span class="o">.</span><span class="n">inv</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">belief</span><span class="o">.</span><span class="n">lam</span><span class="p">)</span>  <span class="c1"># Just for debugging/output</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">mu</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">sigma</span> <span class="o">@</span> <span class="bp">self</span><span class="o">.</span><span class="n">belief</span><span class="o">.</span><span class="n">eta</span>  <span class="c1"># Just for debugging/output</span>

        <span class="c1"># Send message with updated belief to adjacent factors</span>
        <span class="k">for</span> <span class="n">factor_idx</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">adj_factors_idx</span><span class="p">:</span>
            <span class="n">factor</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_nodes</span><span class="p">[</span><span class="n">factor_idx</span><span class="p">]</span>
            <span class="n">eta_message</span><span class="p">,</span> <span class="n">lam_message</span> <span class="o">=</span> <span class="n">factor</span><span class="o">.</span><span class="n">get_message_for</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">idx</span><span class="p">)</span>
            <span class="n">factor</span><span class="o">.</span><span class="n">receive_message_from</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">idx</span><span class="p">,</span> <span class="n">eta</span> <span class="o">-</span> <span class="n">eta_message</span><span class="p">,</span> <span class="n">lam</span> <span class="o">-</span> <span class="n">lam_message</span><span class="p">)</span>
</pre></div>




If the variable has not received any valid messages from a factor, the information matrix is 0. Hence one cannot compute the mean. 
Therefore we need to check if the information matrix is invertable by checking if it's determinat is not zero.

In the last section, the messages from this variable node to each factor_node is updated.

It is necessary to subtract the factor message from the overall estimate in order to fulfill the following equation:
$$ \eta_{x_i \rightarrow f_j} = \sum_{s \in N(i)\setminus j} \eta_{f_s \rightarrow x_i} \text{ and }  \Lambda_{x_i \rightarrow f_j} = \sum_{s \in N(i)\setminus j} \Lambda_{f_s \rightarrow x_i}$$


## Factor Node

The factor node models the dependencies between the variable nodes as a joint gaussian distribution of all adjacent variable nodes.

In this implementation, the factor nodes "registers" itself to it's adjacent variable nodes.





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
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">class</span> <span class="nc">FactorNode</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">adj_variable_nodes</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">VariableNode</span><span class="p">],</span>
                 <span class="n">measurement_fn</span><span class="p">:</span> <span class="n">Callable</span><span class="p">[[</span><span class="n">List</span><span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">],</span> <span class="n">Any</span><span class="p">],</span> <span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">],</span>
                 <span class="n">measurement_noise</span><span class="p">:</span> <span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">,</span>
                 <span class="n">measurement</span><span class="p">:</span> <span class="n">Union</span><span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">,</span> <span class="nb">float</span><span class="p">],</span>
                 <span class="n">jacobian_fn</span><span class="p">:</span> <span class="n">Callable</span><span class="p">[[</span><span class="n">List</span><span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">],</span> <span class="n">Any</span><span class="p">],</span> <span class="n">np</span><span class="o">.</span><span class="n">ndarray</span><span class="p">],</span>
                 <span class="n">args</span><span class="p">:</span> <span class="n">Any</span><span class="p">):</span>
        <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">        Initialize internal variables &amp; adds itself to all adjacent variable nodes</span>
<span class="sd">        :param adj_variable_nodes: all variable nodes, which are adjacent to this factor node</span>
<span class="sd">        :param measurement_fn: the measurement function</span>
<span class="sd">        :param measurement_noise: gaussian covariance matrix representing measurement noise</span>
<span class="sd">        :param measurement: the actual measurement</span>
<span class="sd">        :param jacobian_fn: the jacobian of the measurement function</span>
<span class="sd">        :param args: any additional args for the measurement/jacobian function</span>
<span class="sd">        &quot;&quot;&quot;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">idx</span> <span class="o">=</span> <span class="n">FactorNode</span><span class="o">.</span><span class="n">idx_counter</span>
        <span class="n">FactorNode</span><span class="o">.</span><span class="n">idx_counter</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">adj_variable_node_idxs</span> <span class="o">=</span> <span class="p">[</span><span class="n">v</span><span class="o">.</span><span class="n">idx</span> <span class="k">for</span> <span class="n">v</span> <span class="ow">in</span> <span class="n">adj_variable_nodes</span><span class="p">]</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">measurement_fn</span> <span class="o">=</span> <span class="n">measurement_fn</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">measurement_noise</span> <span class="o">=</span> <span class="n">measurement_noise</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">measurement</span> <span class="o">=</span> <span class="n">measurement</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">jacobian_fn</span> <span class="o">=</span> <span class="n">jacobian_fn</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">args</span> <span class="o">=</span> <span class="n">args</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">adj_variable_messages</span> <span class="o">=</span> <span class="p">{}</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">messages_to_adj_variables</span> <span class="o">=</span> <span class="p">{}</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">linearization_point</span> <span class="o">=</span> <span class="p">[]</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">variable_nodes</span> <span class="o">=</span> <span class="p">[]</span>  <span class="c1"># will be set by the FactorGraph at the end</span>

        <span class="bp">self</span><span class="o">.</span><span class="n">number_of_conditional_variables</span> <span class="o">=</span> <span class="mi">0</span>  <span class="c1"># just as a sanity check</span>
        <span class="k">for</span> <span class="n">variable_node</span> <span class="ow">in</span> <span class="n">adj_variable_nodes</span><span class="p">:</span>
            <span class="n">variable_node</span><span class="o">.</span><span class="n">adj_factors_idx</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">idx</span><span class="p">)</span>  <span class="c1"># bind factor to variable</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">number_of_conditional_variables</span> <span class="o">+=</span> <span class="n">variable_node</span><span class="o">.</span><span class="n">dimensions</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">adj_variable_messages</span><span class="p">[</span><span class="n">variable_node</span><span class="o">.</span><span class="n">idx</span><span class="p">]</span> <span class="o">=</span> <span class="n">deepcopy</span><span class="p">(</span><span class="n">variable_node</span><span class="o">.</span><span class="n">belief</span><span class="p">)</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">messages_to_adj_variables</span><span class="p">[</span><span class="n">variable_node</span><span class="o">.</span><span class="n">idx</span><span class="p">]</span> <span class="o">=</span> <span class="n">GaussianState</span><span class="p">(</span><span class="n">variable_node</span><span class="o">.</span><span class="n">dimensions</span><span class="p">)</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">linearization_point</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">zeros_like</span><span class="p">(</span><span class="n">variable_node</span><span class="o">.</span><span class="n">belief</span><span class="o">.</span><span class="n">eta</span><span class="p">))</span>

        <span class="bp">self</span><span class="o">.</span><span class="n">factor_eta</span> <span class="o">=</span> <span class="kc">None</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span> <span class="o">=</span> <span class="kc">None</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">compute_factor</span><span class="p">()</span>
</pre></div>




### Compute factor

The factor of a factor node does not change over time, iff. the factor is linear.
As this is an implementation supporting none linear factors, it is necessary to recompute the factor each time the linearization point changes.

Usually, the mean is used as the linearization point X_0.

$$
\begin{align}
\eta &= J^T\Sigma^{-1}(d-(h(X_0) - JX_0)\\
\Lambda &= J^T\Sigma^{-1}J\\ \\
h(x) &= \text{measurement function}\\
J &= \text{Jaccobian of measurement function}\\
d &= \text{Measurement}\\
\Sigma &= \text{Measurement Noise}\\
\end{align}
$$

I needed to differentiate between the case where the measurement is a scalar or a vector, as some matrix operations are otherwise not defined.




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
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">class</span> <span class="nc">FactorNode</span>
    <span class="o">...</span>

    <span class="k">def</span> <span class="nf">compute_factor</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">        Computes the factor of the factor node.</span>
<span class="sd">        Should be called, when the linearization point changes.</span>
<span class="sd">        &quot;&quot;&quot;</span>
        <span class="n">jacobian</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">jacobian_fn</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">linearization_point</span><span class="p">,</span> <span class="o">*</span><span class="bp">self</span><span class="o">.</span><span class="n">args</span><span class="p">)</span>

        <span class="n">predicted_measurement</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">measurement_fn</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">linearization_point</span><span class="p">,</span> <span class="o">*</span><span class="bp">self</span><span class="o">.</span><span class="n">args</span><span class="p">)</span>
        <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">measurement</span><span class="p">,</span> <span class="nb">float</span><span class="p">):</span>
            <span class="n">inverse_measurement_noise</span> <span class="o">=</span> <span class="mi">1</span> <span class="o">/</span> <span class="bp">self</span><span class="o">.</span><span class="n">measurement_noise</span>
            <span class="n">lam</span> <span class="o">=</span> <span class="n">inverse_measurement_noise</span> <span class="o">*</span> <span class="n">np</span><span class="o">.</span><span class="n">outer</span><span class="p">(</span><span class="n">jacobian</span><span class="p">,</span> <span class="n">jacobian</span><span class="p">)</span>
            <span class="n">eta</span> <span class="o">=</span> <span class="n">jacobian</span><span class="o">.</span><span class="n">T</span> <span class="o">*</span> <span class="n">inverse_measurement_noise</span> <span class="o">*</span> <span class="p">(</span>
                    <span class="bp">self</span><span class="o">.</span><span class="n">measurement</span> <span class="o">-</span> <span class="p">(</span><span class="n">predicted_measurement</span> <span class="o">-</span> <span class="n">jacobian</span> <span class="o">@</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">linearization_point</span><span class="p">)))</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">inverse_measurement_noise</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">linalg</span><span class="o">.</span><span class="n">inv</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">measurement_noise</span><span class="p">)</span>
            <span class="n">eta</span> <span class="o">=</span> <span class="n">jacobian</span><span class="o">.</span><span class="n">T</span> <span class="o">@</span> <span class="n">inverse_measurement_noise</span> <span class="o">*</span> <span class="p">(</span>
                    <span class="bp">self</span><span class="o">.</span><span class="n">measurement</span> <span class="o">-</span> <span class="p">(</span><span class="n">predicted_measurement</span> <span class="o">-</span> <span class="p">(</span><span class="n">jacobian</span> <span class="o">@</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">linearization_point</span><span class="p">))))</span>
            <span class="n">lam</span> <span class="o">=</span> <span class="n">jacobian</span><span class="o">.</span><span class="n">T</span> <span class="o">@</span> <span class="n">inverse_measurement_noise</span> <span class="o">@</span> <span class="n">jacobian</span>

        <span class="bp">self</span><span class="o">.</span><span class="n">factor_eta</span> <span class="o">=</span> <span class="n">eta</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span> <span class="o">=</span> <span class="n">lam</span>
</pre></div>




Still the factor is a gaussian distribution with eta and lam as its parameters.

### Compute factor to variable messages

Here I want to cite the blog post again. This time Appendix B: Factor to variable message passing:

> To send a message from a factor node to a variable node, the factor aggregates messages from all other adjacent variable nodes before marginalising out all other adjacent variable nodes: 
> $$m_{f_j\rightarrow x_i} = \sum_{X_j \setminus x_i} f_j(X_j) \prod_{k \in N(j)\setminus i} m_{x_k \rightarrow f_j}$$
> To see how this computation is implemented for Gaussian models with the canonical form, consider a factor $$f$$ connected to 3 variable nodes\[$$x_1,x_2,x_3$$\] where we are computing the message to variable $$x_1$$ The factor $$f([x_1,x_2,x_3]) = N^{-1}([x_1,x_2,x_3]; \eta_f, \Lambda_f)$$ is a Gaussian over the variables and can be divided up as follows:
>$$
\eta_f = \begin{bmatrix} \eta_{f_1} \\ \eta_{f_2} \\ \eta_{f_3} \end{bmatrix} \text{and} \Lambda_f = \begin{bmatrix}  
\Lambda_{f_{11}} & \Lambda_{f_{12}}& \Lambda_{f_{13}}\\
\Lambda_{f_{21}} & \Lambda_{f_{22}}& \Lambda_{f_{23}}\\
\Lambda_{f_{31}} & \Lambda_{f_{32}}& \Lambda_{f_{33}}\end{bmatrix}
$$
> The first part of the computation for the message to $$x_1$$, is to take the product of the factor distribution and messages coming from the other adjacent variables nodes ($$x_2$$ and $$x_3$$). This yields a Gaussian with the following parameters:
>$$
\eta_f = \begin{bmatrix} \eta_{f_1} \\ \eta_{f_2}+\eta_{x_2 \rightarrow f} \\ \eta_{f_3}+\eta_{x_3 \rightarrow f} \end{bmatrix} \text{and} \Lambda_f = \begin{bmatrix}  
\Lambda_{f_{11}} & \Lambda_{f_{12}}& \Lambda_{f_{13}}\\
\Lambda_{f_{21}} & \Lambda_{f_{22}}+ \Lambda_{x_2 \rightarrow f} & \Lambda_{f_{23}}\\
\Lambda_{f_{31}} & \Lambda_{f_{32}}& \Lambda_{f_{33}}+ \Lambda_{x_3 \rightarrow f}
\end{bmatrix}
$$
> To complete message passing from this factor, we must marginalise out all variables apart from the variable $x_1$ which is the recipient of the message. The formula for marginalising a Gaussian in the canonical form is given in Eustice et al. For the joint Gaussian distribution over variables a and b parameterized by: 
>$$
\eta = \begin{bmatrix} \eta_a \\ eta_b \end{bmatrix} \text{and} \Lambda = \begin{bmatrix} \Lambda_{aa} & \Lambda_{ab}\\ \Lambda_{ba} & \Lambda_{bb}\end{bmatrix}
$$
> the marginal distribution over a after marginalising out b has parameters:
> $$
\eta_{Ma} = \eta_a - \Lambda_{ab} \Lambda_{bb}^{-1} \eta_b \text{ and } \Lambda_{Ma} = \Lambda_{ab}\Lambda_{bb}^{-1}\Lambda_{ba}
$$
> To apply these formula to the partitioned joint Gaussian parameterized by $$\eta^\prime_{f}$$ and $$\Lambda^\prime_{f}$$, we first reorder the vector and matrix to bring the output variable to the top (in our example the recipient variable $$x_1$$ is already at the top, so we do not need to reorder). Then we identify the subblocks $$a = x_1$$ and $$b = [x_2, x_3]$$ and apply the above marginalization equations to form the parameters of the outgoing message.

As pointed out, there are two-three steps to compute:
1. Product of the incoming messages
2. Reordering
3. Marginalization

I recommend the reader to take some time to compare the formulars with the apropiate code segments to see where what is computed.




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
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">class</span> <span class="nc">FactorNode</span>
    <span class="o">...</span>

    <span class="k">def</span> <span class="nf">compute_outgoing_messages</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">        Computes all factor to variable messages for adjacent variable nodes.</span>
<span class="sd">        The results are stored in a class variable</span>

<span class="sd">        See this blog post Appendix B for the equations: https://gaussianbp.github.io/</span>
<span class="sd">        &quot;&quot;&quot;</span>
        <span class="n">current_eta_factor</span><span class="p">,</span> <span class="n">current_lam_factor</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_eta</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span>
        <span class="n">current_variable_position</span> <span class="o">=</span> <span class="mi">0</span>
        <span class="k">for</span> <span class="n">variable_node_idx</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">adj_variable_node_idxs</span><span class="p">:</span>
            <span class="n">variable_node</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">variable_nodes</span><span class="p">[</span><span class="n">variable_node_idx</span><span class="p">]</span>
            <span class="n">eta_factor</span><span class="p">,</span> <span class="n">lam_factor</span> <span class="o">=</span> <span class="n">current_eta_factor</span><span class="o">.</span><span class="n">copy</span><span class="p">(),</span> <span class="n">current_lam_factor</span><span class="o">.</span><span class="n">copy</span><span class="p">()</span>

            <span class="c1"># For every node take the product of factor and incoming messages</span>
            <span class="n">current_factor_position</span> <span class="o">=</span> <span class="mi">0</span>
            <span class="k">for</span> <span class="n">other_variable_idx</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">adj_variable_node_idxs</span><span class="p">:</span>
                <span class="n">other_variables</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">variable_nodes</span><span class="p">[</span><span class="n">other_variable_idx</span><span class="p">]</span>
                <span class="k">if</span> <span class="n">variable_node_idx</span> <span class="o">!=</span> <span class="n">other_variable_idx</span><span class="p">:</span>
                    <span class="n">start</span> <span class="o">=</span> <span class="n">current_factor_position</span>
                    <span class="n">end</span> <span class="o">=</span> <span class="n">current_factor_position</span> <span class="o">+</span> <span class="n">other_variables</span><span class="o">.</span><span class="n">dimensions</span>
                    <span class="n">eta_factor</span><span class="p">[</span><span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">]</span> <span class="o">+=</span> <span class="bp">self</span><span class="o">.</span><span class="n">adj_variable_messages</span><span class="p">[</span><span class="n">other_variables</span><span class="o">.</span><span class="n">idx</span><span class="p">]</span><span class="o">.</span><span class="n">eta</span>
                    <span class="n">lam_factor</span><span class="p">[</span><span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">,</span> <span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">]</span> <span class="o">+=</span> <span class="bp">self</span><span class="o">.</span><span class="n">adj_variable_messages</span><span class="p">[</span><span class="n">other_variables</span><span class="o">.</span><span class="n">idx</span><span class="p">]</span><span class="o">.</span><span class="n">lam</span>
                <span class="n">current_factor_position</span> <span class="o">+=</span> <span class="n">other_variables</span><span class="o">.</span><span class="n">dimensions</span>

            <span class="c1"># Marginalization to variable node</span>
            <span class="c1"># - First &quot;reorder&quot; variable_nodes&#39;s (short a) elements to the top</span>
            <span class="n">cur_dims</span> <span class="o">=</span> <span class="n">variable_node</span><span class="o">.</span><span class="n">dimensions</span>
            <span class="n">start</span> <span class="o">=</span> <span class="n">current_variable_position</span>
            <span class="n">end</span> <span class="o">=</span> <span class="n">current_variable_position</span> <span class="o">+</span> <span class="n">cur_dims</span>
            <span class="n">eta_a</span> <span class="o">=</span> <span class="n">eta_factor</span><span class="p">[</span><span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">]</span>  <span class="c1"># information vector of variable_node</span>
            <span class="n">eta_b</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">concatenate</span><span class="p">((</span><span class="n">eta_factor</span><span class="p">[:</span><span class="n">start</span><span class="p">],</span> <span class="n">eta_factor</span><span class="p">[</span><span class="n">end</span><span class="p">:]))</span>  <span class="c1"># information vector of the rest</span>

            <span class="n">lam_aa</span> <span class="o">=</span> <span class="n">lam_factor</span><span class="p">[</span><span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">,</span> <span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">]</span>
            <span class="n">lam_ab</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">hstack</span><span class="p">((</span><span class="n">lam_factor</span><span class="p">[</span><span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">,</span> <span class="p">:</span><span class="n">start</span><span class="p">],</span> <span class="n">lam_factor</span><span class="p">[</span><span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">,</span> <span class="n">end</span><span class="p">:]))</span>
            <span class="n">lam_ba</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">vstack</span><span class="p">((</span><span class="n">lam_factor</span><span class="p">[:</span><span class="n">start</span><span class="p">,</span> <span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">],</span> <span class="n">lam_factor</span><span class="p">[</span><span class="n">end</span><span class="p">:,</span> <span class="n">start</span><span class="p">:</span><span class="n">end</span><span class="p">]))</span>
            <span class="n">lam_bb</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">block</span><span class="p">([[</span><span class="n">lam_factor</span><span class="p">[:</span><span class="n">start</span><span class="p">,</span> <span class="p">:</span><span class="n">start</span><span class="p">],</span> <span class="n">lam_factor</span><span class="p">[:</span><span class="n">start</span><span class="p">,</span> <span class="n">end</span><span class="p">:]],</span>
                               <span class="p">[</span><span class="n">lam_factor</span><span class="p">[</span><span class="n">end</span><span class="p">:,</span> <span class="p">:</span><span class="n">start</span><span class="p">],</span> <span class="n">lam_factor</span><span class="p">[</span><span class="n">end</span><span class="p">:,</span> <span class="n">end</span><span class="p">:]]])</span>

            <span class="c1"># - Then marginalize according to https://ieeexplore.ieee.org/document/4020357</span>
            <span class="n">new_message_eta</span> <span class="o">=</span> <span class="n">eta_a</span> <span class="o">-</span> <span class="n">lam_ab</span> <span class="o">@</span> <span class="n">np</span><span class="o">.</span><span class="n">linalg</span><span class="o">.</span><span class="n">inv</span><span class="p">(</span><span class="n">lam_bb</span><span class="p">)</span> <span class="o">@</span> <span class="n">eta_b</span>
            <span class="n">new_message_lam</span> <span class="o">=</span> <span class="n">lam_aa</span> <span class="o">-</span> <span class="n">lam_ab</span> <span class="o">@</span> <span class="n">np</span><span class="o">.</span><span class="n">linalg</span><span class="o">.</span><span class="n">inv</span><span class="p">(</span><span class="n">lam_bb</span><span class="p">)</span> <span class="o">@</span> <span class="n">lam_ba</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">messages_to_adj_variables</span><span class="p">[</span><span class="n">variable_node</span><span class="o">.</span><span class="n">idx</span><span class="p">]</span><span class="o">.</span><span class="n">eta</span> <span class="o">=</span> <span class="n">new_message_eta</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">messages_to_adj_variables</span><span class="p">[</span><span class="n">variable_node</span><span class="o">.</span><span class="n">idx</span><span class="p">]</span><span class="o">.</span><span class="n">lam</span> <span class="o">=</span> <span class="n">new_message_lam</span>

            <span class="n">current_variable_position</span> <span class="o">+=</span> <span class="n">variable_node</span><span class="o">.</span><span class="n">dimensions</span>
</pre></div>




## Factor Graph

The factor graph has not much logic inside it. It just calls the functions of the appropriate nodes.

At the beginning, it will give all nodes a complete list of all factors/variable nodes, which they need to send their messages.




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
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">class</span> <span class="nc">FactorGraph</span>
    <span class="o">...</span>

    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">variable_nodes</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">VariableNode</span><span class="p">],</span> <span class="n">factor_nodes</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">FactorNode</span><span class="p">]):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">variable_nodes</span> <span class="o">=</span> <span class="n">variable_nodes</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">factor_nodes</span> <span class="o">=</span> <span class="n">factor_nodes</span>
        <span class="k">for</span> <span class="n">v</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">variable_nodes</span><span class="p">:</span>
            <span class="n">v</span><span class="o">.</span><span class="n">factor_nodes</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_nodes</span>
        <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_nodes</span><span class="p">:</span>
            <span class="n">f</span><span class="o">.</span><span class="n">variable_nodes</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">variable_nodes</span>
</pre></div>




### Synchronous Iteration

Currently, I only implemented the synchronous iteration, but others are possible.
To be sure, I also relinearize the factors before each iteration.




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
.output_html .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span><span class="k">class</span> <span class="nc">FactorGraph</span>
    <span class="o">...</span>

    <span class="k">def</span> <span class="nf">synchronous_iteration</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&quot;&quot;&quot;</span>
<span class="sd">        Triggers a single synchronous iteration over all nodes (factor and variable nodes)</span>
<span class="sd">        &quot;&quot;&quot;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">relinearize_factors</span><span class="p">()</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">compute_all_messages</span><span class="p">()</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">update_all_beliefs</span><span class="p">()</span>
</pre></div>




# Usage example

To see the Gaussian Belief Propagation in action, I would recommend you to read my next blog article about Contour Fitting.

# References

1. Ortiz, J.; Evans, T. & Davison, A. J. A visual introduction to Gaussian Belief Propagation CoRR, 2021, abs/2107.02308 [link](https://gaussianbp.github.io/)
2. Bishop, C. M. Pattern Recognition and Machine Learning (Information Science and Statistics) Springer-Verlag, 2006 [pdf](https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf)
3. Barber, D. Bayesian Reasoning and Machine Learning Cambridge University Press, 2012 [pdf](http://web4.cs.ucl.ac.uk/staff/D.Barber/textbook/090310.pdf)

