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



    
![png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABSYAAARZCAIAAABYM0m8AAAACXBIWXMAAAuJAAALiQE3ycutAAAgAElEQVR4nOzde3yU9Z3o8d8zk0wSQGIRuQkVCqIiilyKpWqtrYqtZetybL22W3fbKr3Y6qtbj62V9bW79fTsWVfPWau9261arR5ra+XQVeu1pUVurqioCCqlAUQkQCCZZOY5fwyGGMJVnjwzyfv96ovOPPMk84XWyyfPb35PFMdxAAAAAA60TNoDAAAAQM8kuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwB6i0cffTSKokcffTTtQQCgt5DcAJC4W2+9NYqiBQsWlJ7OmTPnH/7hH5J+0+9+97u33npr0u+yG5dffvmkSZMGDBjQp0+fo48++h/+4R+2bNnS8YSWlpYrr7xy2LBhdXV1J5xwwoMPPpjWqACQkCiO47RnAIAe7tZbb7344oufeuqpKVOmhBC+9KUv3XTTTUn/I3j8+PEDBw7seE27WCzm8/lcLpfJdMfP3E866aTJkyePGTOmtrZ28eLFP/7xj6dMmfL444+3v/v5559/zz33fPWrXz3iiCNuvfXWp5566pFHHjnppJO6YTYA6B5VaQ8AAOybOI6bm5vr6ur29QszmUxtbW0SI3XpySef7Ph09OjRX/va1+bPn/++970vhDB//vw777zzX/7lX772ta+FED796U+PHz/+61//+h/+8IdumxAAkmZhOQB0q8985jM33XRTCCF6S+l4sVi84YYbjjnmmNra2sGDB19yySVvvvlm+1eNHDnyYx/72G9/+9spU6bU1dV973vfCyH85Cc/+dCHPjRo0KCamppx48bdfPPNHc9/9tlnH3vssdJbfPCDHwxdfZb77rvvnjx5cl1d3cCBAy+66KLVq1d3nLNfv36rV68+++yz+/Xrd+ihh37ta18rFArtJzQ0NCxbtqy1tXUvf+MjR44MIWzcuLH09J577slms5///OdLT2tra//u7/5u3rx5q1at2stvCADlz1VuAOhWl1xyyV/+8pcHH3zwZz/7WafjpfXnl1122cqVK//93/998eLFv//976urq0snvPDCC+eff/4ll1zyuc997sgjjwwh3Hzzzcccc8xf/dVfVVVV3X///V/4wheKxeIXv/jFEMINN9zw5S9/uV+/ft/85jdDCIMHD955ktLbvfe9773uuuvWrl174403/v73v1+8ePHBBx9cOqFQKEyfPv2EE074X//rfz300EP/+q//Onr06FmzZpVeveqqq37605+uXLmy1NJdamtr27hxYz6fX7p06dVXX33QQQdNnTq19NLixYvHjh3bv3//9pNLLy1ZsmTEiBH792cLAOVGcgNAt5o2bdrYsWMffPDBiy66qP3gk08++cMf/vD222+/4IILSkdOPfXUM8888+67724/snz58rlz506fPr39qx577LH25eVf+tKXzjzzzOuvv76U3GefffbVV19dunbd5Ritra1XXnnl+PHjH3/88dJq85NOOuljH/vYv/3bv1177bWlc5qbm88999xvfetbIYRLL7100qRJP/rRj9qTe28sWLBg2rRppcdHHnnkr3/96wEDBpSeNjQ0DB06tOPJpad/+ctf9v77A0CZs7AcANJ3991319fXn3766evfMnny5H79+j3yyCPt54waNapjb4cQ2nu7sbFx/fr1p5xyyooVKxobG/fmHRcsWLBu3bovfOEL7Z/uPuuss4466qgHHnig42mXXnpp++OTTz55xYoV7U9vvfXWOI53c4k7hDBu3LgHH3zwvvvu+/rXv963b9+OO5Zv27atpqam48mlSbZt27Y38wNARXCVGwDS99JLLzU2Ng4aNKjT8XXr1rU/HjVqVKdXf//738+ePXvevHlbt25tP9jY2FhfX7/Hd3z11VdDCKUF6u2OOuqojnue1dbWHnrooe1P3/Wud3X8ePne6N+//2mnnRZC+PjHP37HHXd8/OMfX7Ro0YQJE0IIdXV1LS0tHU9ubm4OHX6OAAA9gOQGgPQVi8VBgwbdfvvtnY53LN5OLfryyy9/+MMfPuqoo66//voRI0bkcrk5c+b827/9W7FYPFBTZbPZA/WtQggzZ8781Kc+deedd5aSe+jQoR13awshNDQ0hBCGDRt2AN8UANIluQGgu7XvUt5u9OjRDz300Iknnrj313jvv//+lpaWX//61+9+97tLRzquQu/yXTo6/PDDQwgvvPDChz70ofaDL7zwQul4ElpaWorFYvu69+OPP/6RRx7ZtGlT+w5qf/rTn0rHExoAALqfz3IDQHfr27dv6HC7rBDCJz/5yUKh8I//+I8dTytt972rb1K6BB3HcelpY2PjT37yk07vspsvnzJlyqBBg2655Zb21d3/7//9v+eff/6ss87ay9/F7m8StnHjxk4v/fCHPyy9b+npOeecUygUvv/975eetrS0/OQnPznhhBNsVw5AT+IqNwB0t8mTJ4cQLrvssunTp2ez2fPOO++UU0655JJLrrvuuiVLlpxxxhnV1dUvvfTS3XfffeONN55zzjldfpMzzjgjl8vNmDHjkksu2bJlyw9+8INBgwaV1ma3v8vNN9/8T//0T2PGjBk0aFDHq9khhOrq6u985zsXX3zxKaeccv7555duEjZy5MjLL798L38Xu79J2KOPPnrZZZedc845RxxxRD6ff+KJJ+69994pU6a076B+wgknfOITn7jqqqvWrVs3ZsyYn/70p6+88sqPfvSjvXx3AKgIkhsAutvMmTO//OUv33nnnbfddlscx+edd14I4ZZbbpk8efL3vve9b3zjG1VVVSNHjrzoootOPPHEXX2TI4888p577rn66qu/9rWvDRkyZNasWYceeujf/u3ftp9wzTXXvPrqq//zf/7PzZs3n3LKKZ2SO4Twmc98pk+fPv/jf/yPK6+8sm/fvn/913/9ne98p/2m3O/Qsccee+qpp/7qV79qaGiI43j06NHXXHPN3//93+dyufZz/uM//uNb3/rWz372szfffPO44477zW9+84EPfOCAvDsAlImofUEaAAAAcAD5LDcAAAAkQnIDAABAIiQ3AAAAJKLck/vxxx+fMWPGsGHDoii67777dnXao48+OmnSpJqamjFjxtx6663dOCAAAAB0rdyTu6mpacKECTfddNNuzlm5cuVZZ5116qmnLlmy5Ktf/epnP/vZ3/72t902IQAAAHSpYnYsj6Lol7/85dlnn73zS1deeeUDDzywdOnS0tPzzjtv48aNc+fO7d4BAQAA4G3K/Sr33pg3b95pp53W/nT69Onz5s1LcR4AAAAIIVSlPcABsGbNmsGDB7c/HTx48KZNm7Zt21ZXV9fxtJaWlpaWltLjYrG4YcOGQw45JIqibp0VAACAMhDH8ebNm4cNG5bJJHgpuick91667rrrrr322rSnAAAAoFysWrVq+PDhyX3/npDcQ4YMWbt2bfvTtWvX9u/fv9Ml7hDCVVdddcUVV5QeNzY2vvvd7161alX//v27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AAD0iOI4TnuGDzBnzpyrr776u9/9bgihWq2OHz/+S1/60l/91V+d6POVSmX48OHf/e53P/3pT5/oM3v37m1padmzZ8+wYcMSGRoAAIA6VpsqrPdV7lKptGLFivnz5/d8m8lk5s+fv3Tp0pP8koMHD5bL5REjRhxzvaura+8RkpoYAAAAQgj1n9zvvPNOpVI5//zze6+cf/7527dvP8kv+epXvzp27NjeSu/1zW9+s+U948ePT2RcAAAAeE+9J/fp+ta3vvXjH//4pz/9abFYPOatr33ta3ves2XLllTGAwAAYODIpT3ABzjvvPOy2ezbb7/de+Xtt98ePXr0cT/87W9/+1vf+taTTz555ZVXvv/dpqampqampAYFAACAo9X7KnehUJg1a9ZTTz3V8221Wn3qqaeuueaa93/yf//v//23f/u3ixcvbmtrq+2MAAAAcBz1vsodQrj33nvvuuuutra22bNnL1q06MCBA5/5zGdCCJ/+9KcvuOCCb37zmyGEv//7v//617/+7//+7xMmTOh50nvIkCFDhgxJeXQAAAAGsAZI7k9+8pM7d+78+te/vn379unTpy9evLhnN7XNmzdnModW6R988MFSqXTnnXf2/qr77rvvb/7mb1IZGAAAAEJDnMudBOdyAwAADGTO5QYAAIAGJrkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIbAAAAEiG5AQAAIBGSGwAAABIhuQEAACARkhsAAAASIbkBAAAgEZIb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
)
    


And this end this blog entry. Now you can experiment with the code and make your own FactorGraphs.
