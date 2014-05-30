from flask import Flask
from flask import request

app = Flask(__name__)

from problem1 import solutionA as pr1_A
from problem1 import solutionB as pr1_B
from problem2 import solutionA as pr2_A


@app.route("/")
def hello():
    return "Hello World!"

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def to_int_array(arr):
    arr_ints = [ int(x) if is_int(x) else None for x in arr.split(',') ]
    return [ x for x in arr_ints if x is not None ]

@app.route("/most_consecutive/<arr>")
def most_consecutive_item(arr):
    arr_ints = to_int_array(arr)
    res = pr1_A.findMostConsecutivelyRepeatingValue_ideal(arr_ints)
    return 'Input Array = {}<br>Value with the most consecutive appearances = {}<br>Number of consecutive appearances = {}'\
        .format(arr_ints, res[0] if res else 'None', res[1] if res else 'None')

@app.route("/most_frequent/<arr>")
def most_frequent_item(arr):
    arr_ints = to_int_array(arr)
    res = pr1_B.findMostFrequentValue_ideal(arr_ints)
    return 'Input Array = {}<br>Most frequent value = {}<br>Number of appearances = {}'\
        .format(arr_ints, res[0] if res else 'None', res[1] if res else 'None')

@app.route("/merge_sort/")
def merge_sort():
    list1 = request.args.get('list1')
    list2 = request.args.get('list2')
    input1 = to_int_array(list1)
    input2 = to_int_array(list2)
    res = pr2_A.merge_sort_ideal(list(input1), list(input2), key=lambda x: x)
    return 'Input List 1 = {}<br>Input List 2 = {}<br>Merged Result = {}'\
        .format(input1, input2, res)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_debugger=True, use_reloader=True )
