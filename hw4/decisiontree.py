"""Learn to estimate functions from examples. (Chapters 18-20)"""

from utils import *
import os
import copy, heapq, math, random
from collections import defaultdict

#______________________________________________________________________________

def rms_error(predictions, targets):
    return math.sqrt(ms_error(predictions, targets))

def ms_error(predictions, targets):
    return mean([(p - t)**2 for p, t in zip(predictions, targets)])

def mean_error(predictions, targets):
    return mean([abs(p - t) for p, t in zip(predictions, targets)])

def mean_boolean_error(predictions, targets):
    return mean([(p != t)   for p, t in zip(predictions, targets)])

#______________________________________________________________________________
class DataSet:
    """A data set for a machine learning problem.  It has the following fields:

    d.examples    A list of examples.  Each one is a list of attribute values.
    d.attrs       A list of integers to index into an example, so example[attr]
                  gives a value. Normally the same as range(len(d.examples[0])).
    d.attrnames   Optional list of mnemonic names for corresponding attrs.
    d.target      The attribute that a learning algorithm will try to predict.
                  By default the final attribute.
    d.inputs      The list of attrs without the target.
    d.values      A list of lists: each sublist is the set of possible
                  values for the corresponding attribute. If initially None,
                  it is computed from the known examples by self.setproblem.
                  If not None, an erroneous value raises ValueError.
    d.distance    A function from a pair of examples to a nonnegative number.
                  Should be symmetric, etc. Defaults to mean_boolean_error
                  since that can handle any field types.
    d.name        Name of the data set (for output display only).
    d.source      URL or other source where the data came from.

    Normally, you call the constructor and you're done; then you just
    access fields like d.examples and d.target and d.inputs."""

    def __init__(self, examples=None, attrs=None, attrnames=None, target=-1,
                 inputs=None, values=None, distance=mean_boolean_error,
                 name='', source='', exclude=()):
        """Accepts any of DataSet's fields.  Examples can also be a
        string or file from which to parse examples using parse_csv.
        Optional parameter: exclude, as documented in .setproblem().
        >>> DataSet(examples='1, 2, 3')
        <DataSet(): 1 examples, 3 attributes>
        """
        update(self, name=name, source=source, values=values, distance=distance)
        # Initialize .examples from string or list or data directory
        if isinstance(examples, str):
            self.examples = parse_csv(examples)
        elif examples is None:
            self.examples = parse_csv(DataFile(name+'.csv').read())
        else:
            self.examples = examples
        # Attrs are the indices of examples, unless otherwise stated.
        if not attrs and self.examples:
            attrs = range(len(self.examples[0]))
        self.attrs = attrs
        # Initialize .attrnames from string, list, or by default
        if isinstance(attrnames, str):
            self.attrnames = attrnames.split()
        else:
            self.attrnames = attrnames or attrs
        self.setproblem(target, inputs=inputs, exclude=exclude)

    def setproblem(self, target, inputs=None, exclude=()):
        """Set (or change) the target and/or inputs.
        This way, one DataSet can be used multiple ways. inputs, if specified,
        is a list of attributes, or specify exclude as a list of attributes
        to not use in inputs. Attributes can be -n .. n, or an attrname.
        Also computes the list of possible values, if that wasn't done yet."""
        self.target = self.attrnum(target)
        exclude = map(self.attrnum, exclude)
        if inputs:
            self.inputs = removeall(self.target, inputs)
        else:
            self.inputs = [a for a in self.attrs
                           if a != self.target and a not in exclude]
        if not self.values:
            self.values = map(unique, zip(*self.examples))
        self.check_me()

    def check_me(self):
        "Check that my fields make sense."
        assert len(self.attrnames) == len(self.attrs)
        assert self.target in self.attrs
        assert self.target not in self.inputs
        assert set(self.inputs).issubset(set(self.attrs))
        map(self.check_example, self.examples)

    def add_example(self, example):
        "Add an example to the list of examples, checking it first."
        self.check_example(example)
        self.examples.append(example)

    def check_example(self, example):
        "Raise ValueError if example has any invalid values."
        if self.values:
            for a in self.attrs:
                if example[a] not in self.values[a]:
                    raise ValueError('Bad value %s for attribute %s in %s' %
                                     (example[a], self.attrnames[a], example))

    def attrnum(self, attr):
        "Returns the number used for attr, which can be a name, or -n .. n-1."
        if attr < 0:
            return len(self.attrs) + attr
        elif isinstance(attr, str):
            return self.attrnames.index(attr)
        else:
            return attr

    def sanitize(self, example):
       "Return a copy of example, with non-input attributes replaced by None."
       return [attr_i if i in self.inputs else None
               for i, attr_i in enumerate(example)]

    def __repr__(self):
        return '<DataSet(%s): %d examples, %d attributes>' % (
            self.name, len(self.examples), len(self.attrs))

#______________________________________________________________________________

def parse_csv(input, delim=','):
    r"""Input is a string consisting of lines, each line has comma-delimited
    fields.  Convert this into a list of lists.  Blank lines are skipped.
    Fields that look like numbers are converted to numbers.
    The delim defaults to ',' but '\t' and None are also reasonable values.
    >>> parse_csv('1, 2, 3 \n 0, 2, na')
    [[1, 2, 3], [0, 2, 'na']]
    """
    lines = [line for line in input.splitlines() if line.strip()]
    return [map(num_or_str, line.split(delim)) for line in lines]

#______________________________________________________________________________



class DecisionLeaf:

	def __init__(self, result):
		self.result = result

	def __call__(self, example):
		return self.result

class DecisionFork:
	def __init__(self, attr, attrname = None, branckes = None):
		update(self, attr=attr, attrname = attrname or attr,
				branches = branches or {})

	def __call__(self, example):

		attrvalue = example[self.attr]
		return self.branckes[attrvalue](example)
	
	def add(self, val, subtree):
		self.branches[val] = subtree

	def display(self, indent = 0):
		name = self.attrname
		print 'Test', name
		for(val, subtree) in self.branches.items():
			print ' '*4*indent, name, '=', val, '==>',
			subtree.display(indent+1)

	def __repr__(self):
		return('DecisionFork(%r, %r, %r)'
			% (self.attr, self.attrname, self.branches))

def DecisionTreeLearner(dataset):

	target, values = dataset.target, dataset.values

	def decision_tree_learning(examples, attrs, parent_examples=()):
		if len(examples)==0:
			return plurality_value(parent_examples)
		elif all_same_class(examples):
			DecisionLeaf(examples[0][target])
		elif len(attrs)==0:
			return plurality_value(examples)
		else:
			A = choose_attribute(attrs, examples)
			tree = DecisionFork(A, dataset.attrnames[A])
			for(v_k, exs) in split_by(A, examples):
				subtree = decision_tree_learning(
					exs, removeall(A, attrs), examples)
				tree.add(v_k, subtree)
		return tree
			




	def plurality_value(examples):
		groups = itertools.groupby(sorted(examples))
		def _auxfun((item,iterable)):
			return len(list(iterable)), -L.index(item)
		return max(groups, key=_auxfun)[0];



	def all_same_class(examples):
		value = examples[0][target]
		return all(e[target] == value for e in examples)

	def choose_attribute(attrs, examples):
		return argmax_random_tie(attrs, lambda a: information_gain(a, examples))

	def information_gain(attrs, examples):
		def I(examples):
			return information_contect([count(target, v, examples)
						   for v in values[target]])
		N = float(len(examples))
		remainder = sum((len(examples_i) / N) * I(examples_i)
				for (v, examplex_i) in split_by(attr, examples))
		return I(examples)-remainder
	
	return decision_tree_learning(dataset.examples, dataset.inputs)
		
	
	def information_content(values):
		prob = normalize(removeall(0, values))
		return sum(-p * log2(p) for p in prob)

	def split_by(attr, examples):
		return [(v, [e for e in examples if e[attr] ==v])
			for v in values[attr]]

	return decision_tree_learning(dataset.examples, dataset.inputs)

def cross_validation(learner, dataset, k=10, trials=1):
    """Do k-fold cross_validate and return their mean.
    That is, keep out 1/k of the examples for testing on each of k runs.
    Shuffle the examples first; If trials>1, average over several shuffles."""
    if k is None:
        k = len(dataset.examples)
    if trials > 1:
        return mean([cross_validation(learner, dataset, k, trials=1)
                     for t in range(trials)])
    else:
        n = len(dataset.examples)
        random.shuffle(dataset.examples)
        return mean([train_and_test(learner, dataset, i*(n/k), (i+1)*(n/k))
                     for i in range(k)])


def BankDataSet(examples=None):
	return DataSet(name='bank', target = 'class',
			attrnames='variance skewness curtosis entropy class')

if __name__ == '__main__':
	bank = BankDataSet()
	bank_tree = DecisionTreeLearner(bank)
	ban_tree.display()
