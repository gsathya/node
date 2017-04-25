// Copyright 2017 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Flags: --no-stress-opt

console.time();
console.timeEnd();

console.time("abcd");
console.timeEnd({ toString: () => "ab" + "cd" });

console.time("a");
console.timeEnd("b");

console.time("a", "b");
console.timeEnd("a", "b");

console.log("log", "more");
console.warn("warn", { toString: () => 2 });
console.error("error");
console.debug("debug");
console.info("info");
