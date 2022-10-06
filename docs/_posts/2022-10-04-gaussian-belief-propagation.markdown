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

# Gaussian Belief Propagation - An Implementation guide
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

        <span class="c1"># Ensure that matrix is positive-semi-definite</span>
        <span class="n">lam</span> <span class="o">=</span> <span class="p">(</span><span class="n">lam</span> <span class="o">+</span> <span class="n">lam</span><span class="o">.</span><span class="n">T</span><span class="p">)</span> <span class="o">/</span> <span class="mf">2.</span>
        <span class="n">lam</span> <span class="o">-=</span> <span class="n">np</span><span class="o">.</span><span class="n">identity</span><span class="p">(</span><span class="n">lam</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span> <span class="o">*</span> <span class="mf">1e-6</span>

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

        <span class="bp">self</span><span class="o">.</span><span class="n">number_of_conditional_variables</span> <span class="o">=</span> <span class="mi">0</span>
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

        <span class="n">inverse_measurement_noise</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">linalg</span><span class="o">.</span><span class="n">inv</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">measurement_noise</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">factor_eta</span> <span class="o">=</span> <span class="n">jacobian</span><span class="o">.</span><span class="n">T</span> <span class="o">@</span> <span class="n">inverse_measurement_noise</span> <span class="o">*</span> <span class="p">(</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">measurement</span> <span class="o">-</span> <span class="p">(</span><span class="n">predicted_measurement</span> <span class="o">-</span> <span class="p">(</span><span class="n">jacobian</span> <span class="o">@</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">linearization_point</span><span class="p">)</span><span class="o">.</span><span class="n">flatten</span><span class="p">())))</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">factor_eta</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_eta</span><span class="o">.</span><span class="n">flatten</span><span class="p">()</span>

        <span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span> <span class="o">=</span> <span class="n">jacobian</span><span class="o">.</span><span class="n">T</span> <span class="o">@</span> <span class="n">inverse_measurement_noise</span> <span class="o">@</span> <span class="n">jacobian</span>

        <span class="c1"># Ensure that matrix is positive-semi-definite</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span> <span class="o">=</span> <span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span> <span class="o">+</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span><span class="o">.</span><span class="n">T</span><span class="p">)</span> <span class="o">/</span> <span class="mf">2.</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span> <span class="o">+=</span> <span class="n">np</span><span class="o">.</span><span class="n">identity</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span> <span class="o">*</span> <span class="mf">1e-6</span>
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
> To complete message passing from this factor, we must marginalise out all variables apart from the variable $$x_1$$ which is the recipient of the message. The formula for marginalising a Gaussian in the canonical form is given in Eustice et al. For the joint Gaussian distribution over variables a and b parameterized by: 
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
        <span class="n">current_variable_position</span> <span class="o">=</span> <span class="mi">0</span>
        <span class="k">for</span> <span class="n">variable_node_idx</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">adj_variable_node_idxs</span><span class="p">:</span>
            <span class="n">variable_node</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">variable_nodes</span><span class="p">[</span><span class="n">variable_node_idx</span><span class="p">]</span>
            <span class="n">eta_factor</span><span class="p">,</span> <span class="n">lam_factor</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_eta</span><span class="o">.</span><span class="n">copy</span><span class="p">(),</span> <span class="bp">self</span><span class="o">.</span><span class="n">factor_lam</span><span class="o">.</span><span class="n">copy</span><span class="p">()</span>

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

            <span class="c1"># Ensure that matrix is positive-semi-definite</span>
            <span class="n">new_message_lam</span> <span class="o">=</span> <span class="p">(</span><span class="n">new_message_lam</span> <span class="o">+</span> <span class="n">new_message_lam</span><span class="o">.</span><span class="n">T</span><span class="p">)</span> <span class="o">/</span> <span class="mf">2.</span>
            <span class="n">new_message_lam</span> <span class="o">+=</span> <span class="n">np</span><span class="o">.</span><span class="n">identity</span><span class="p">(</span><span class="n">new_message_lam</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span> <span class="o">*</span> <span class="mf">1e-6</span>

            <span class="bp">self</span><span class="o">.</span><span class="n">messages_to_adj_variables</span><span class="p">[</span><span class="n">variable_node_idx</span><span class="p">]</span><span class="o">.</span><span class="n">eta</span> <span class="o">=</span> <span class="n">new_message_eta</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">messages_to_adj_variables</span><span class="p">[</span><span class="n">variable_node_idx</span><span class="p">]</span><span class="o">.</span><span class="n">lam</span> <span class="o">=</span> <span class="n">new_message_lam</span>

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

