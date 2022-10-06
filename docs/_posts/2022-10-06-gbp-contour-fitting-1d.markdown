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


    
![png](data:image/png;base64,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
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
    <span class="n">height_measurement</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">random</span><span class="p">()</span> <span class="o">*</span> <span class="mf">0.1</span>
    <span class="n">x_pos</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">random</span><span class="o">.</span><span class="n">random</span><span class="p">()</span>
    <span class="k">if</span> <span class="n">x_pos</span> <span class="o">&lt;</span> <span class="mf">0.5</span><span class="p">:</span>
        <span class="n">height_measurement</span> <span class="o">+=</span> <span class="mf">0.7</span>
    <span class="k">else</span><span class="p">:</span>
        <span class="n">height_measurement</span> <span class="o">+=</span> <span class="mf">0.2</span>
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
    <span class="n">use_huber</span> <span class="o">=</span> <span class="kc">False</span>
    <span class="n">num_var</span> <span class="o">=</span> <span class="mi">20</span>
    <span class="n">num_measurements</span> <span class="o">=</span> <span class="mi">12</span>
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



    
![png](data:image/png;base64,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
)
    

