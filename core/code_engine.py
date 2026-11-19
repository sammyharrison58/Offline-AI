import re
from typing import Dict, Any, List, Optional, Tuple

_CODE_TOKEN_RE = re.compile(r'[a-z0-9_\-\+\#\.]+')
_CODE_STOPWORDS = frozenset({"how", "to", "write", "a", "an", "the", "in", "for", "code", "function", "program", "script", "algorithm", "solution", "solve", "can", "you", "please", "me", "give", "implement", "create"})

LANG_ALIASES = {
    "py": "python",
    "python": "python",
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "c++": "cpp",
    "cpp": "cpp",
    "c": "c",
    "rust": "rust",
    "rs": "rust",
    "go": "golang",
    "golang": "golang",
    "sql": "sql",
    "bash": "bash",
    "shell": "bash",
    "sh": "bash",
    "html": "html",
    "css": "css",
    "java": "java",
    "c#": "csharp",
    "csharp": "csharp",
    "ruby": "ruby",
    "rb": "ruby",
    "php": "php"
}

CODE_RECIPES: List[Dict[str, Any]] = [
    {
        "id": "py_two_sum",
        "languages": ["python"],
        "keywords": ["two sum", "target sum", "pair sum", "array two sum", "hash map two sum"],
        "title": "Two Sum (Hash Map O(n))",
        "description": "Finds two indices in an integer array whose values add up to a target sum using a hash map in linear O(n) time.",
        "code": """```python
def two_sum(nums, target):
    seen = {}
    for idx, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], idx]
        seen[num] = idx
    return []

nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(f"Indices: {result}")
print(f"Values: {nums[result[0]]} + {nums[result[1]]} = {target}")
```"""
    },
    {
        "id": "py_reverse_linked_list",
        "languages": ["python"],
        "keywords": ["reverse linked list", "reverse singly linked list", "linked list reverse"],
        "title": "Reverse Singly Linked List (Iterative O(n) Time, O(1) Space)",
        "description": "Reverses a singly linked list in-place by updating pointer directions in linear time.",
        "code": """```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    prev = None
    curr = head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev

def print_list(node):
    vals = []
    while node:
        vals.append(str(node.val))
        node = node.next
    print(" -> ".join(vals))

head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
print("Original:")
print_list(head)
reversed_head = reverse_linked_list(head)
print("Reversed:")
print_list(reversed_head)
```"""
    },
    {
        "id": "py_binary_search",
        "languages": ["python"],
        "keywords": ["binary search", "bsearch", "binary search array", "logarithmic search"],
        "title": "Binary Search (O(log n) Time, Iterative)",
        "description": "Performs logarithmic search on a sorted list to locate the target value index.",
        "code": """```python
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid]
        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

sorted_data = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
target = 23
idx = binary_search(sorted_data, target)
print(f"Element {target} found at index: {idx}")
```"""
    },
    {
        "id": "py_quicksort",
        "languages": ["python"],
        "keywords": ["quicksort", "quick sort", "partition sort"],
        "title": "Quicksort Algorithm (In-Place Partitioning)",
        "description": "Divide-and-conquer sorting algorithm selecting a pivot and partitioning elements.",
        "code": """```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

data = [38, 27, 43, 3, 9, 82, 10]
sorted_arr = quicksort(data)
print(f"Sorted array: {sorted_arr}")
```"""
    },
    {
        "id": "py_lru_cache",
        "languages": ["python"],
        "keywords": ["lru cache", "least recently used", "cache implementation", "lru"],
        "title": "LRU Cache (Least Recently Used) O(1) Get and Put",
        "description": "Implements an LRU cache using a doubly linked list and hash map for O(1) access and eviction.",
        "code": """```python
class DNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = DNode()
        self.tail = DNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = DNode(key, value)
        self.cache[key] = node
        self._add_to_front(node)
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

cache = LRUCache(2)
cache.put(1, 100)
cache.put(2, 200)
print("Key 1:", cache.get(1))
cache.put(3, 300)
print("Key 2 (evicted):", cache.get(2))
print("Key 3:", cache.get(3))
```"""
    },
    {
        "id": "py_valid_parentheses",
        "languages": ["python"],
        "keywords": ["valid parentheses", "balanced parentheses", "stack brackets", "parentheses matching"],
        "title": "Valid Parentheses Checker (Stack O(n))",
        "description": "Validates that brackets in a string are closed in the correct order using a stack.",
        "code": """```python
def is_valid_parentheses(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top_elem = stack.pop() if stack else '#'
            if mapping[char] != top_elem:
                return False
        else:
            stack.append(char)
    return not stack

test_cases = ["()[]{}", "([{}])", "(]", "([)]", "{[]}"]
for test in test_cases:
    print(f"'{test}': {is_valid_parentheses(test)}")
```"""
    },
    {
        "id": "py_palindrome",
        "languages": ["python"],
        "keywords": ["palindrome", "check palindrome", "is palindrome", "palindrome string"],
        "title": "Palindrome String Verification",
        "description": "Checks if an alphanumeric string reads identically forward and backward ignoring case.",
        "code": """```python
def is_palindrome(text: str) -> bool:
    clean = [c.lower() for c in text if c.isalnum()]
    return clean == clean[::-1]

examples = ["A man, a plan, a canal: Panama", "race a car", "Was it a car or a cat I saw?", "No 'x' in Nixon"]
for ex in examples:
    print(f"'{ex}' -> {is_palindrome(ex)}")
```"""
    },
    {
        "id": "py_bfs_dfs_graph",
        "languages": ["python"],
        "keywords": ["bfs", "dfs", "graph traversal", "breadth first search", "depth first search"],
        "title": "Graph Traversal: BFS & DFS in Python",
        "description": "Breadth-First Search using a queue and Depth-First Search using recursion or stack.",
        "code": """```python
from collections import deque

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

def dfs(graph, start, visited=None, order=None):
    if visited is None:
        visited = set()
    if order is None:
        order = []
    visited.add(start)
    order.append(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, order)
    return order

print("BFS traversal:", bfs(graph, 'A'))
print("DFS traversal:", dfs(graph, 'A'))
```"""
    },
    {
        "id": "js_debounce",
        "languages": ["javascript", "typescript"],
        "keywords": ["debounce", "debounce function", "debounce user input", "javascript debounce"],
        "title": "Debounce Function (JavaScript / TypeScript)",
        "description": "Postpones function execution until a specified delay has elapsed since the last call.",
        "code": """```javascript
function debounce(fn, delay = 300) {
    let timerId = null;
    return function (...args) {
        if (timerId !== null) {
            clearTimeout(timerId);
        }
        timerId = setTimeout(() => {
            fn.apply(this, args);
            timerId = null;
        }, delay);
    };
}

const logSearch = (query) => console.log(`Searching for: ${query}`);
const debouncedSearch = debounce(logSearch, 400);

debouncedSearch("al");
debouncedSearch("alex");
debouncedSearch("alexander");
```"""
    },
    {
        "id": "js_throttle",
        "languages": ["javascript", "typescript"],
        "keywords": ["throttle", "throttle function", "javascript throttle", "throttle scroll"],
        "title": "Throttle Function (JavaScript / TypeScript)",
        "description": "Guarantees a function executes at most once per specified time interval.",
        "code": """```javascript
function throttle(fn, limit = 250) {
    let inThrottle = false;
    return function (...args) {
        if (!inThrottle) {
            fn.apply(this, args);
            inThrottle = true;
            setTimeout(() => {
                inThrottle = false;
            }, limit);
        }
    };
}

const onScroll = () => console.log("Scroll event processed at:", Date.now());
const throttledScroll = throttle(onScroll, 500);

window.addEventListener("scroll", throttledScroll);
```"""
    },
    {
        "id": "js_deep_clone",
        "languages": ["javascript", "typescript"],
        "keywords": ["deep clone", "deep copy", "clone object", "deep clone object"],
        "title": "Deep Clone Object (Handles Nested Objects, Arrays, Dates, Sets)",
        "description": "Creates an independent deep copy of complex nested structures handling circular references via WeakMap.",
        "code": """```javascript
function deepClone(obj, hash = new WeakMap()) {
    if (obj === null || typeof obj !== "object") return obj;
    if (obj instanceof Date) return new Date(obj.getTime());
    if (obj instanceof RegExp) return new RegExp(obj.source, obj.flags);
    if (hash.has(obj)) return hash.get(obj);

    const copy = Array.isArray(obj) ? [] : Object.create(Object.getPrototypeOf(obj));
    hash.set(obj, copy);

    for (const key of Reflect.ownKeys(obj)) {
        copy[key] = deepClone(obj[key], hash);
    }
    return copy;
}

const original = { a: 1, b: { c: [2, 3, 4] }, date: new Date() };
const clone = deepClone(original);
clone.b.c.push(5);
console.log("Original:", JSON.stringify(original));
console.log("Clone:", JSON.stringify(clone));
```"""
    },
    {
        "id": "js_event_emitter",
        "languages": ["javascript", "typescript"],
        "keywords": ["event emitter", "pub sub", "event bus", "custom events"],
        "title": "Event Emitter (Pub/Sub Pattern in JavaScript)",
        "description": "Implements an event bus allowing subscription, one-time listener, unsubscription, and event emission.",
        "code": """```javascript
class EventEmitter {
    constructor() {
        this.events = new Map();
    }

    on(event, listener) {
        if (!this.events.has(event)) {
            this.events.set(event, []);
        }
        this.events.get(event).push(listener);
        return () => this.off(event, listener);
    }

    once(event, listener) {
        const wrapper = (...args) => {
            this.off(event, wrapper);
            listener(...args);
        };
        return this.on(event, wrapper);
    }

    emit(event, ...args) {
        if (!this.events.has(event)) return false;
        const listeners = [...this.events.get(event)];
        listeners.forEach(fn => fn(...args));
        return true;
    }

    off(event, listener) {
        if (!this.events.has(event)) return;
        const filtered = this.events.get(event).filter(fn => fn !== listener);
        if (filtered.length > 0) {
            this.events.set(event, filtered);
        } else {
            this.events.delete(event);
        }
    }
}

const bus = new EventEmitter();
const unsub = bus.on("userLogin", name => console.log(`Welcome, ${name}!`));
bus.emit("userLogin", "Commander");
unsub();
```"""
    },
    {
        "id": "cpp_invert_binary_tree",
        "languages": ["cpp", "c++"],
        "keywords": ["invert binary tree", "invert tree", "mirror binary tree", "cpp invert binary tree"],
        "title": "Invert Binary Tree (C++ Recursive & Iterative)",
        "description": "Swaps left and right subtrees for every node in a binary tree.",
        "code": """```cpp
#include <iostream>
#include <queue>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* invertTree(TreeNode* root) {
    if (root == nullptr) return nullptr;
    TreeNode* temp = root->left;
    root->left = invertTree(root->right);
    root->right = invertTree(temp);
    return root;
}

void printLevelOrder(TreeNode* root) {
    if (!root) return;
    std::queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* curr = q.front();
        q.pop();
        std::cout << curr->val << " ";
        if (curr->left) q.push(curr->left);
        if (curr->right) q.push(curr->right);
    }
    std::cout << "\\n";
}

int main() {
    TreeNode* root = new TreeNode(4);
    root->left = new TreeNode(2);
    root->right = new TreeNode(7);
    root->left->left = new TreeNode(1);
    root->left->right = new TreeNode(3);
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(9);

    std::cout << "Original tree: ";
    printLevelOrder(root);

    root = invertTree(root);

    std::cout << "Inverted tree: ";
    printLevelOrder(root);
    return 0;
}
```"""
    },
    {
        "id": "cpp_reverse_linked_list",
        "languages": ["cpp", "c++"],
        "keywords": ["reverse linked list cpp", "cpp reverse linked list", "linked list cpp"],
        "title": "Reverse Singly Linked List (C++ In-Place)",
        "description": "Inverts pointer direction for a singly linked list with zero extra memory allocation.",
        "code": """```cpp
#include <iostream>

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* curr = head;
    while (curr != nullptr) {
        ListNode* nextNode = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nextNode;
    }
    return prev;
}

void printList(ListNode* head) {
    ListNode* curr = head;
    while (curr != nullptr) {
        std::cout << curr->val << (curr->next ? " -> " : "\\n");
        curr = curr->next;
    }
}

int main() {
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);

    std::cout << "Original: ";
    printList(head);

    head = reverseList(head);

    std::cout << "Reversed: ";
    printList(head);
    return 0;
}
```"""
    },
    {
        "id": "cpp_thread_pool",
        "languages": ["cpp", "c++"],
        "keywords": ["thread pool", "cpp thread pool", "multithreading cpp", "worker threads"],
        "title": "Thread Pool Pattern (C++17 std::thread & condition_variable)",
        "description": "Manages a pool of persistent worker threads executing enqueued callable tasks.",
        "code": """```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <future>

class ThreadPool {
public:
    ThreadPool(size_t threads) : stop(false) {
        for (size_t i = 0; i < threads; ++i) {
            workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lock(this->queue_mutex);
                        this->cv.wait(lock, [this] {
                            return this->stop || !this->tasks.empty();
                        });
                        if (this->stop && this->tasks.empty()) return;
                        task = std::move(this->tasks.front());
                        this->tasks.pop();
                    }
                    task();
                }
            });
        }
    }

    template<class F, class... Args>
    auto enqueue(F&& f, Args&&... args) 
        -> std::future<typename std::invoke_result<F, Args...>::type> {
        using return_type = typename std::invoke_result<F, Args...>::type;

        auto task = std::make_shared<std::packaged_task<return_type()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...)
        );
        std::future<return_type> res = task->get_future();
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            if (stop) throw std::runtime_error("enqueue on stopped ThreadPool");
            tasks.emplace([task]() { (*task)(); });
        }
        cv.notify_one();
        return res;
    }

    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            stop = true;
        }
        cv.notify_all();
        for (std::thread &worker: workers) {
            if (worker.joinable()) worker.join();
        }
    }

private:
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queue_mutex;
    std::condition_variable cv;
    bool stop;
};

int main() {
    ThreadPool pool(4);
    std::vector<std::future<int>> results;

    for (int i = 0; i < 8; ++i) {
        results.emplace_back(
            pool.enqueue([i] {
                return i * i;
            })
        );
    }

    for (auto &&result : results) {
        std::cout << result.get() << " ";
    }
    std::cout << "\\n";
    return 0;
}
```"""
    },
    {
        "id": "rust_quicksort",
        "languages": ["rust"],
        "keywords": ["rust quicksort", "quicksort rust", "rust sort"],
        "title": "Quicksort Algorithm in Rust (Generic & In-Place)",
        "description": "Safe, idiomatic in-place quicksort implemented generically for any Ord type.",
        "code": """```rust
pub fn quicksort<T: Ord>(slice: &mut [T]) {
    if slice.len() <= 1 {
        return;
    }
    let pivot_idx = partition(slice);
    let (left, right) = slice.split_at_mut(pivot_idx);
    quicksort(left);
    quicksort(&mut right[1..]);
}

fn partition<T: Ord>(slice: &mut [T]) -> usize {
    let len = slice.len();
    let pivot_idx = len - 1;
    let mut i = 0;
    for j in 0..pivot_idx {
        if slice[j] <= slice[pivot_idx] {
            slice.swap(i, j);
            i += 1;
        }
    }
    slice.swap(i, pivot_idx);
    i
}

fn main() {
    let mut data = vec![42, 17, 88, 3, 65, 29, 94, 11];
    println!("Unsorted: {:?}", data);
    quicksort(&mut data);
    println!("Sorted:   {:?}", data);
}
```"""
    },
    {
        "id": "rust_concurrency",
        "languages": ["rust"],
        "keywords": ["rust concurrency", "rust arc mutex", "rust threads", "thread spawn rust"],
        "title": "Thread-Safe Shared State in Rust (Arc<Mutex<T>>)",
        "description": "Demonstrates safe cross-thread shared state using Atomic Reference Counting and Mutex.",
        "code": """```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter_clone = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter_clone.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Final Counter Result: {}", *counter.lock().unwrap());
}
```"""
    },
    {
        "id": "go_worker_pool",
        "languages": ["golang", "go"],
        "keywords": ["go worker pool", "goroutines worker pool", "channels worker pool", "golang concurrency"],
        "title": "Concurrent Worker Pool in Go (Goroutines & Channels)",
        "description": "Spawns concurrent worker goroutines reading from a jobs channel and posting to results.",
        "code": """```go
package main

import (
	"fmt"
	"time"
)

func worker(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		fmt.Printf("Worker %d starting job %d\\n", id, j)
		time.Sleep(50 * time.Millisecond)
		results <- j * 2
	}
}

func main() {
	const numJobs = 6
	const numWorkers = 3

	jobs := make(chan int, numJobs)
	results := make(chan int, numJobs)

	for w := 1; w <= numWorkers; w++ {
		go worker(w, jobs, results)
	}

	for j := 1; j <= numJobs; j++ {
		jobs <- j
	}
	close(jobs)

	for a := 1; a <= numJobs; a++ {
		res := <-results
		fmt.Printf("Result collected: %d\\n", res)
	}
}
```"""
    },
    {
        "id": "go_http_server",
        "languages": ["golang", "go"],
        "keywords": ["go http server", "golang rest api", "go web server", "go http api"],
        "title": "Minimal REST API Server in Go (net/http)",
        "description": "Standard library HTTP server with JSON response encoding and routing.",
        "code": """```go
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type StatusResponse struct {
	Status  string `json:"status"`
	Version string `json:"version"`
	Offline bool   `json:"offline"`
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	resp := StatusResponse{
		Status:  "operational",
		Version: "2.2.6",
		Offline: true,
	}
	json.NewEncoder(w).Encode(resp)
}

func main() {
	http.HandleFunc("/api/status", statusHandler)
	fmt.Println("Server listening on http://localhost:8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```"""
    },
    {
        "id": "sql_second_highest_salary",
        "languages": ["sql"],
        "keywords": ["second highest salary", "nth highest salary", "highest salary sql", "dense_rank salary"],
        "title": "Find Second Highest Salary (SQL Window Function & Subquery)",
        "description": "Retrieves the second distinct maximum salary handling ties and null fallbacks.",
        "code": """```sql
SELECT (
    SELECT DISTINCT salary 
    FROM Employee 
    ORDER BY salary DESC 
    LIMIT 1 OFFSET 1
) AS SecondHighestSalary;

SELECT salary AS SecondHighestSalary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM Employee
) ranked
WHERE rnk = 2
LIMIT 1;
```"""
    },
    {
        "id": "sql_delete_duplicates",
        "languages": ["sql"],
        "keywords": ["delete duplicates", "delete duplicate rows", "remove duplicate sql"],
        "title": "Delete Duplicate Rows Keeping Smallest ID (SQL)",
        "description": "Removes duplicate records from a table while retaining the primary original row.",
        "code": """```sql
DELETE p1 
FROM Person p1
JOIN Person p2 
  ON p1.email = p2.email 
 AND p1.id > p2.id;

WITH RankedDuplicates AS (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) as row_num
    FROM Person
)
DELETE FROM Person 
WHERE id IN (SELECT id FROM RankedDuplicates WHERE row_num > 1);
```"""
    },
    {
        "id": "html_css_login_card",
        "languages": ["html", "css"],
        "keywords": ["login card", "login form", "modern login", "html css login", "dark mode login"],
        "title": "Modern Dark-Mode Login Card (HTML5 & Modern CSS Grid/Flexbox)",
        "description": "Production-ready, responsive glassmorphism dark-mode authentication card.",
        "code": """```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nexus Authentication</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
  body {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #030712;
    color: #f3f4f6;
  }
  .card {
    background: rgba(17, 24, 39, 0.85);
    border: 1px solid rgba(0, 240, 255, 0.25);
    border-radius: 16px;
    padding: 36px;
    width: 100%;
    max-width: 400px;
    box-shadow: 0 8px 32px rgba(0, 240, 255, 0.15);
    backdrop-filter: blur(12px);
  }
  h2 { font-size: 24px; font-weight: 700; color: #00f0ff; margin-bottom: 24px; text-align: center; }
  .field { margin-bottom: 18px; }
  label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: #9ca3af; }
  input {
    width: 100%;
    padding: 12px 16px;
    background: #1f2937;
    border: 1px solid #374151;
    border-radius: 8px;
    color: #fff;
    outline: none;
    transition: border-color 0.2s;
  }
  input:focus { border-color: #00f0ff; }
  button {
    width: 100%;
    padding: 12px;
    margin-top: 10px;
    background: linear-gradient(135deg, #00f0ff, #3b82f6);
    border: none;
    border-radius: 8px;
    font-weight: 700;
    color: #000;
    cursor: pointer;
    transition: opacity 0.2s;
  }
  button:hover { opacity: 0.9; }
</style>
</head>
<body>
  <div class="card">
    <h2>NEXUS LOGIN</h2>
    <form>
      <div class="field">
        <label>Operator ID / Email</label>
        <input type="email" placeholder="admin@nexus.ai" required>
      </div>
      <div class="field">
        <label>Access Key</label>
        <input type="password" placeholder="••••••••••••" required>
      </div>
      <button type="submit">AUTHORIZE & ENTER</button>
    </form>
  </div>
</body>
</html>
```"""
    },
    {
        "id": "bash_backup_script",
        "languages": ["bash", "shell"],
        "keywords": ["bash backup", "backup script", "backup directory", "shell script backup"],
        "title": "Automated Directory Backup Script with Timestamp (Bash)",
        "description": "Creates compressed gzip tarballs with rotation and error checking in Bash.",
        "code": """```bash
#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-./data}"
BACKUP_DEST="${2:-./backups}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="backup_${TIMESTAMP}.tar.gz"

mkdir -p "${BACKUP_DEST}"

echo "Starting backup of ${SOURCE_DIR} to ${BACKUP_DEST}/${ARCHIVE_NAME}..."
tar -czf "${BACKUP_DEST}/${ARCHIVE_NAME}" -C "${SOURCE_DIR}" .

echo "Backup completed successfully: $(ls -lh "${BACKUP_DEST}/${ARCHIVE_NAME}")"

echo "Pruning backups older than 14 days..."
find "${BACKUP_DEST}" -name "backup_*.tar.gz" -type f -mtime +14 -delete
echo "Done."
```"""
    },
    {
        "id": "c_dynamic_array",
        "languages": ["c"],
        "keywords": ["dynamic array c", "c vector", "malloc realloc array", "vector in c"],
        "title": "Dynamic Array Vector in C (malloc/realloc Growth)",
        "description": "Custom dynamically resizing array vector with amortized O(1) appending in pure C.",
        "code": """```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int* data;
    size_t size;
    size_t capacity;
} Vector;

Vector* vector_create() {
    Vector* v = (Vector*)malloc(sizeof(Vector));
    v->size = 0;
    v->capacity = 4;
    v->data = (int*)malloc(v->capacity * sizeof(int));
    return v;
}

void vector_push(Vector* v, int val) {
    if (v->size == v->capacity) {
        v->capacity *= 2;
        v->data = (int*)realloc(v->data, v->capacity * sizeof(int));
    }
    v->data[v->size++] = val;
}

int vector_get(Vector* v, size_t index) {
    if (index >= v->size) {
        fprintf(stderr, "Index out of bounds\\n");
        exit(1);
    }
    return v->data[index];
}

void vector_free(Vector* v) {
    free(v->data);
    free(v);
}

int main() {
    Vector* v = vector_create();
    for (int i = 1; i <= 10; ++i) {
        vector_push(v, i * 10);
    }
    for (size_t i = 0; i < v->size; ++i) {
        printf("%d ", vector_get(v, i));
    }
    printf("\\n");
    vector_free(v);
    return 0;
}
```"""
    }
]

class CodeKnowledgeEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CodeKnowledgeEngine, cls).__new__(cls)
            cls._instance._init_engine()
        return cls._instance

    def _init_engine(self):
        self.recipes = CODE_RECIPES
        self.inverted_index: Dict[str, List[int]] = {}
        self.lang_index: Dict[str, List[int]] = {}
        for idx, recipe in enumerate(self.recipes):
            for lang in recipe.get("languages", []):
                l_clean = lang.lower()
                if l_clean not in self.lang_index:
                    self.lang_index[l_clean] = []
                self.lang_index[l_clean].append(idx)
            for kw in recipe.get("keywords", []):
                for tok in _CODE_TOKEN_RE.findall(kw.lower()):
                    if tok not in _CODE_STOPWORDS:
                        if tok not in self.inverted_index:
                            self.inverted_index[tok] = []
                        if idx not in self.inverted_index[tok]:
                            self.inverted_index[tok].append(idx)

    def search_code(self, query: str) -> Optional[Dict[str, Any]]:
        clean = query.lower().strip()
        tokens = [t for t in _CODE_TOKEN_RE.findall(clean) if t not in _CODE_STOPWORDS]
        if not tokens:
            return None

        target_lang = None
        for tok in tokens:
            if tok in LANG_ALIASES:
                target_lang = LANG_ALIASES[tok]
                break

        candidate_scores: Dict[int, int] = {}
        for tok in tokens:
            if tok in self.inverted_index:
                for idx in self.inverted_index[tok]:
                    candidate_scores[idx] = candidate_scores.get(idx, 0) + 3

        for idx, recipe in enumerate(self.recipes):
            if target_lang and target_lang in recipe.get("languages", []):
                candidate_scores[idx] = candidate_scores.get(idx, 0) + 4
            for kw in recipe.get("keywords", []):
                if kw in clean:
                    candidate_scores[idx] = candidate_scores.get(idx, 0) + 12

        if not candidate_scores:
            return None

        best_idx = max(candidate_scores.keys(), key=lambda i: candidate_scores[i])
        if candidate_scores[best_idx] >= 6:
            return self.recipes[best_idx]
        return None

    def format_solution(self, recipe: Dict[str, Any]) -> str:
        lines = [
            f"### 💻 {recipe.get('title')}",
            f"\n**Language / Ecosystem:** `{', '.join(recipe.get('languages', []))}`",
            f"**Overview:** {recipe.get('description')}\n",
            recipe.get("code", "").strip()
        ]
        return "\n".join(lines)
