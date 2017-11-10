// Copyright (c) 2015-2017, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/* Utilities
 * @desc Utilities for use by the package.
 */
export function extend<T, U>(first: T, second: U) : T & U {
    let result = <T & U> {};
    for (let item in first) {
        (<any>result)[item] = (<any>first)[item];
    }
    for (let item in second) {
        (<any>result)[item] = (<any>second)[item];
    }
    return result;
}
