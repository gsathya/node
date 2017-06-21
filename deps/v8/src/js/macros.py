# Copyright 2006-2009 the V8 project authors. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of Google Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Dictionary that is passed as defines for js2c.py.
# Used for defines that must be defined for all native JS files.

define NONE        = 0;
define READ_ONLY   = 1;
define DONT_ENUM   = 2;
define DONT_DELETE = 4;

# 2^53 - 1
define kMaxSafeInteger = 9007199254740991;

# 2^32 - 1
define kMaxUint32 = 4294967295;

# Type query macros.
#
# Note: We have special support for typeof(foo) === 'bar' in the compiler.
#       It will *not* generate a runtime typeof call for the most important
#       values of 'bar'.
macro IS_ARRAY(arg)             = (%_IsArray(arg));
macro IS_ARRAYBUFFER(arg)       = (%_ClassOf(arg) === 'ArrayBuffer');
macro IS_BOOLEAN(arg)           = (typeof(arg) === 'boolean');
macro IS_DATE(arg)              = (%IsDate(arg));
macro IS_ERROR(arg)             = (%_ClassOf(arg) === 'Error');
macro IS_FUNCTION(arg)          = (%IsFunction(arg));
macro IS_GENERATOR(arg)         = (%_ClassOf(arg) === 'Generator');
macro IS_GLOBAL(arg)            = (%_ClassOf(arg) === 'global');
macro IS_MAP(arg)               = (%_IsJSMap(arg));
macro IS_MAP_ITERATOR(arg)      = (%_IsJSMapIterator(arg));
macro IS_NULL(arg)              = (arg === null);
macro IS_NULL_OR_UNDEFINED(arg) = (arg == null);
macro IS_NUMBER(arg)            = (typeof(arg) === 'number');
macro IS_OBJECT(arg)            = (typeof(arg) === 'object');
macro IS_PROXY(arg)             = (%_IsJSProxy(arg));
macro IS_SCRIPT(arg)            = (%_ClassOf(arg) === 'Script');
macro IS_SET(arg)               = (%_IsJSSet(arg));
macro IS_SET_ITERATOR(arg)      = (%_IsJSSetIterator(arg));
macro IS_SHAREDARRAYBUFFER(arg) = (%_ClassOf(arg) === 'SharedArrayBuffer');
macro IS_STRING(arg)            = (typeof(arg) === 'string');
macro IS_SYMBOL(arg)            = (typeof(arg) === 'symbol');
macro IS_TYPEDARRAY(arg)        = (%_IsTypedArray(arg));
macro IS_UNDEFINED(arg)         = (arg === (void 0));
macro IS_WEAKMAP(arg)           = (%_IsJSWeakMap(arg));
macro IS_WEAKSET(arg)           = (%_IsJSWeakSet(arg));

# Macro for ES queries of the type: "Type(O) is Object."
macro IS_RECEIVER(arg) = (%_IsJSReceiver(arg));

# Macro for ES queries of the type: "IsCallable(O)"
macro IS_CALLABLE(arg) = (typeof(arg) === 'function');

# Macro for ES6 CheckObjectCoercible
# Will throw a TypeError of the form "[functionName] called on null or undefined".
macro CHECK_OBJECT_COERCIBLE(arg, functionName) = if (IS_NULL(%IS_VAR(arg)) || IS_UNDEFINED(arg)) throw %make_type_error(kCalledOnNullOrUndefined, functionName);

# Inline macros. Use %IS_VAR to make sure arg is evaluated only once.
macro NUMBER_IS_NAN(arg) = (%IS_VAR(arg) !== arg);
macro NUMBER_IS_FINITE(arg) = (%_IsSmi(%IS_VAR(arg)) || ((arg == arg) && (arg != 1/0) && (arg != -1/0)));
macro TO_BOOLEAN(arg) = (!!(arg));
macro TO_INTEGER(arg) = (%_ToInteger(arg));
macro INVERT_NEG_ZERO(arg) = ((arg) + 0);
macro TO_LENGTH(arg) = (%_ToLength(arg));
macro TO_STRING(arg) = (%_ToString(arg));
macro TO_NUMBER(arg) = (%_ToNumber(arg));
macro TO_OBJECT(arg) = (%_ToObject(arg));
macro HAS_OWN_PROPERTY(obj, key) = (%_Call(ObjectHasOwnProperty, obj, key));

# Private names.
macro GET_PRIVATE(obj, sym) = (obj[sym]);
macro SET_PRIVATE(obj, sym, val) = (obj[sym] = val);

# To avoid ES2015 Function name inference.
macro ANONYMOUS_FUNCTION(fn) = (0, (fn));

# Constants.  The compiler constant folds them.
define INFINITY = (1/0);
define UNDEFINED = (void 0);

# Must match PropertyFilter in property-details.h
define PROPERTY_FILTER_NONE = 0;

# Use for keys, values and entries iterators.
define ITERATOR_KIND_KEYS = 1;
define ITERATOR_KIND_VALUES = 2;
define ITERATOR_KIND_ENTRIES = 3;

macro FIXED_ARRAY_GET(array, index) = (%_FixedArrayGet(array, (index) | 0));
macro FIXED_ARRAY_SET(array, index, value) = (%_FixedArraySet(array, (index) | 0, value));
# TODO(adamk): Find a more robust way to force Smi representation.
macro FIXED_ARRAY_SET_SMI(array, index, value) = (FIXED_ARRAY_SET(array, index, (value) | 0));

macro ORDERED_HASH_TABLE_BUCKET_COUNT(table) = (FIXED_ARRAY_GET(table, 2));
macro ORDERED_HASH_TABLE_ELEMENT_COUNT(table) = (FIXED_ARRAY_GET(table, 0));
macro ORDERED_HASH_TABLE_SET_ELEMENT_COUNT(table, count) = (FIXED_ARRAY_SET_SMI(table, 0, count));
macro ORDERED_HASH_TABLE_DELETED_COUNT(table) = (FIXED_ARRAY_GET(table, 1));
macro ORDERED_HASH_TABLE_SET_DELETED_COUNT(table, count) = (FIXED_ARRAY_SET_SMI(table, 1, count));
macro ORDERED_HASH_TABLE_BUCKET_AT(table, bucket) = (FIXED_ARRAY_GET(table, 3 + (bucket)));
macro ORDERED_HASH_TABLE_SET_BUCKET_AT(table, bucket, entry) = (FIXED_ARRAY_SET(table, 3 + (bucket), entry));

macro ORDERED_HASH_TABLE_HASH_TO_BUCKET(hash, numBuckets) = (hash & ((numBuckets) - 1));

macro ORDERED_HASH_SET_ENTRY_TO_INDEX(entry, numBuckets) = (3 + (numBuckets) + ((entry) << 1));
macro ORDERED_HASH_SET_KEY_AT(table, entry, numBuckets) = (FIXED_ARRAY_GET(table, ORDERED_HASH_SET_ENTRY_TO_INDEX(entry, numBuckets)));
macro ORDERED_HASH_SET_CHAIN_AT(table, entry, numBuckets) = (FIXED_ARRAY_GET(table, ORDERED_HASH_SET_ENTRY_TO_INDEX(entry, numBuckets) + 1));

macro ORDERED_HASH_MAP_ENTRY_TO_INDEX(entry, numBuckets) = (3 + (numBuckets) + ((entry) * 3));
macro ORDERED_HASH_MAP_KEY_AT(table, entry, numBuckets) = (FIXED_ARRAY_GET(table, ORDERED_HASH_MAP_ENTRY_TO_INDEX(entry, numBuckets)));
macro ORDERED_HASH_MAP_VALUE_AT(table, entry, numBuckets) = (FIXED_ARRAY_GET(table, ORDERED_HASH_MAP_ENTRY_TO_INDEX(entry, numBuckets) + 1));
macro ORDERED_HASH_MAP_CHAIN_AT(table, entry, numBuckets) = (FIXED_ARRAY_GET(table, ORDERED_HASH_MAP_ENTRY_TO_INDEX(entry, numBuckets) + 2));

# Must match OrderedHashTable::kNotFound.
define NOT_FOUND = -1;

# Check whether debug is active.
define DEBUG_IS_ACTIVE = (%_DebugIsActive() != 0);
