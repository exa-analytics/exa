/*"""
===============
num.js
===============
Numerical utilities; mimicking numpy's functionality in some cases.
*/
'use strict';


define([], function() {
    var linspace = function(min, max, n) {
        /*"""
        linspace
        --------------
        Create a linearly spaced array of the form [min, max) with n linearly
        spaced elements.

        Args:
            min (number): Starting number
            max (number): Ending number (not inclusive)
            n (number): Number of elements

        Returns:
            array (array): Array of values
        */
        var step = (max - min) / (n - 1);
        var element = min;
        var array = [element];
        for (let i=0; i<n; i++) {
            element += step;
            array.push(element);
        };
        return array;
    };

    return {
        'linspace': linspace,
    };
});
