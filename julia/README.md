# Julia: the TL;DR
 
Julia is a [functional programming](https://en.wikipedia.org/wiki/Functional_programming) language.
 
## What is it?
 
It that was first developed in 2012 for 'scientific computing'. Julia purports to be as intuitive and simple to learn as Python, with the speed of C.
 
The creators of Julia said:
 
_“We want the speed of C with the dynamism of Ruby. We want a language that’s homoiconic, with true macros like Lisp, but with obvious, familiar mathematical notation like Matlab. We want something as usable for general programming as Python, as easy for statistics as R, as natural for string processing as Perl, as powerful for linear algebra as Matlab, as good at gluing programs together as the shell. Something that is dirt simple to learn, yet keeps the most serious hackers happy.”_

A lofty goal! 
 
There are **three** fundamental syntactic differences when we compare Julia to Python: type hierarchies, multiple dispatch and user defined types.

### Type Hierarchies
 
To fully leverage Julia's speed, it's important to take advantage of Julia's type hierarchies. Julia has two different types: concrete and abstract types. Concrete types are the types we all know and love: `String`, `Bool`, `Int64`, `Float64` etc. They can be instantiated and used in computations.
 
Meanwhile, abstract types CANNOT be instantiated. They are essentially 'containers' for grouping together similar kinds of data i.e. `Union{}`, `AbstractFloat`, `Real`, and `Any`. We love an abstract type because functions defined to act on an abstract type can act on all the subtypes of the abstract type.
 
For example, suppose you need an array-like data structure. In Julia, you can define your own abstract array type. Then, all functions where you define the type abstract array will work smoothly. Contrast this to Python - if you're working with an array that is not a `numpy` defined array and want to call `numpy` functions on it, you'll likely face errors.    

### Multiple Dispatch
 
Multiple dispatch refers to when a function behaves differently depending on the types of its arguments. See below:
 
```
# Verbose definition
function f(x)
   return x^2 % 4
end
# Mathematical notation
f(x) = x^2 % 4
# Like a Python lambda
f = x -> x^2 % 4
```
 
In python, we _could_ use a bunch of if statements to deal with parameter types:
 
```
def f_py(x):
   if type(x) == string:
       x = float(x)
   if type(x) == float:
       x = ceil(x)
   return x**2 % 4
```
 
And indeed, we could take this python approach in Julia:
 
```
function f_py(x)
   if isa(x, String)
       x = parse(Float64, x)
   end
   if isa(x, Float64)
       x = ceil(Int64,x)
   end
   x^2 % 4
end
```
 
But the best approach would be to define multiple type based methods to the function:
 
```
f(x::Int64) = x^2 % 4
f(x::Float64) = f(ceil(Int64, x))
f(x::String) = f(parse(Float64, x))
```
 
Although Julia is fundamentally faster than Python, using multiple dispatch (or assigning multiple methods to a function) is even faster than pythonic Julia.

### User Defined Types

Finally, and perhaps uncomfortably enough (depending on how you program in Python), Julia is not object oriented. Instead, Julia leverages structs, which are simply user defined types aka a collection of named types. 
 
For example:
 
```
struct NBAPlayer
   name::String
   height::Int   
   points::Float64
   rebounds::Float64
   assists::Float64
end
 
doncic = NBAPlayer("Luka Doncic", 79, 24.4, 8.5, 7.1)
```
where you can access fields using dot notation i.e. `doncic.height`, `doncic.name` etc. You can pass your user defined types into functions, in the same way you do concrete or abstract types:
 
```
function Base.show(io::IO, player::NBAPlayer)
   print(io, player.name)
   print(io, ": ")
   print(io, (player.points, player.rebounds, player.assists))
end
```
 
So, getting comfortable with Julia means getting comfortable with a new syntax, functional programming, being scrupulous with type definitions and introducing multiple dispatch. And most scandelously of all, prepare to start indexing at 1. 
 
## So what?
 
I've found learning a bit of Julia interesting for two main reasons:
 
1. **It solidifies Python fundamentals:** As Julia tutorials tend to walk through the language's fundamentals, you find yourself comparing the two languages and how they might differ. Simply put, it's hard to pick up on i.e. a type hierarchy without going back to fundamental types and their purpose.
 
2. **It's good to keep up with the Joneses:** We all know it's helpful to keep up with popular areas of data science, including programming. The newsletter Data Machina, a weekly digest of AI/ML curiosities and other amenities, officially has a _Love from Julia_ section. A quick search of 'julia' on GitHub revealed at least 16k repositories written in Julia, over 36 million commits and 181k issues. And finally, [StackOverflow](https://discourse.julialang.org/t/julia-got-in-the-most-loved-languages-of-the-stackoverflow-survey/45260) named it the "most loved langauge" in 2020.  
 
## Libraries
 
Some familiar libraries in julia that are relevant include:

0. [**DataFrames.jl**](https://dataframes.juliadata.org/stable/#:~:text=jl%3F-,DataFrames.,(in%20Python)%20and%20data.): It's very similar to `pandas` or `dplyr` (in R).   

1. [**ScikitLearn.jl**](https://cstjean.github.io/ScikitLearn.jl/stable/): This is a julia wrapper for `scikitlearn` - it doesn't have to same level of intgration with `DataFrames.jl` as `pandas` does with `scikitlearn` in python. 

2. [**Plots.jl**](https://docs.juliaplots.org/latest/) and [**VegaLite.jl**](https://www.queryverse.org/VegaLite.jl/stable/): For plotting, `Plots.jl` is akin to `matplotlib`. `VegaLite.jl` follows 'grammer of graphics' and is plotting ++ (incl. interactives).

3. [**TextAnalysis.jl**](https://github.com/JuliaText/TextAnalysis.jl): For text analysis including TF-IDF, topic models like LDA, and integration with other packages like `WordTokenizers.jl`.   

4. [**Agents.jl**](https://juliadynamics.github.io/Agents.jl/stable/): A pure Julia framework for agent based modelling. 

Other helpful [data science specific libraries can be found here](https://dataframes.juliadata.org/stable/#DataFrames.jl-and-the-Julia-Data-Ecosystem).


## Links
 
0. [This youtube video](https://www.youtube.com/watch?v=YoyvGw5qPww) walking you through how to download Julia for mac and install it for Jupyter notebook.
 
1. [This very thorough step-by-step tutorial](https://syl1.gitbook.io/julia-language-a-concise-tutorial/language-core/getting-started) on areas from data types and custom structures to managing errors, performance and even developing your own Julia packages.
 
2. [This repo with a ton of exercises](https://github.com/JuliaAcademy/JuliaTutorials) split into both introductory-tutorials and more-advanced-materials.
 
3. [These LeetCode exercises for Julia](https://cn.julialang.org/LeetCode.jl/dev/democards/problems/problems/1.two-sum/) - for when you're a bit more familiar with the syntax.
 
4. [These StackOverflow Julia questions](https://stackoverflow.com/questions/tagged/julia), although there is admittedly (and unsurprisingly) much less on debugging in Julia on StackOverflow than Python.