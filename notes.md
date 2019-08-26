# Introduction to Programming

## Meta

## Lecture 1: 2019-08-01

## Lecture 2: 2019-08-06

### Limits of (Efficient) Computation

**Church Thesis**

* There can be problems that can not be computed by any machine/are not computable.

* Example: Halting Problem 

**P/NP type problems**

* Polynomial time/non-polynomial time
* Non-polynomial time problems (NP-hard):
  * Travelling Salesman
  * Burglar Problem

### Python

#### Types of Literals

* Integer
* Float
* Boolean
* String

> Exponentials are **right-associative: evaluated right to left**

```py
>>> 3**2**3
6561
```

### To Read

* Precedence and associativity of operators
* ~~Ones-complement and Twos-complement~~
* ~~Sign representation~~
* ~~Floating point arithmetic and representation~~

## Lecture 3: 2019-08-08

* Expression: Has to return something
* Statement: Not necessary
* In Python, all integers that are not one hold boolean value False, unlike other programming lang.

## Lecture 4

* 0.375 * 2 = 0.75 => 0
  0.75 * 2 = 1.5 => 1
  0.5 * 2 = 1.0 => 1
  therefore, (0.375)<sub>10</sub> = (0.011)<sub>2</sub>

* 0.1 * 2 = 0.2 => 0
  0.2 * 2 = 0.4 => 0
  0.4 * 2 = 0.8 => 0
  0.8 * 2 = 1.6 => 1
  0.6 * 2 = 1.2 => 1
  0.2 * 2 = 0.4 => 0
  ...
  therefore (0.1)<sub>10</sub> = (0.0001100110011...)<sub>2</sub>
* Bias representation
* 17 = 10001, 17 >> 2 => 100 = 4