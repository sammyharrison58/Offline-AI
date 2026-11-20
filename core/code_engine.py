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
    },
    {
        "id": "py_merge_sort",
        "languages": ["python"],
        "keywords": ["merge sort", "mergesort", "merge sort algorithm", "divide conquer sort"],
        "title": "Merge Sort Algorithm (O(n log n) Guaranteed Time)",
        "description": "Stable divide-and-conquer sorting algorithm that recursively splits arrays and merges sorted halves.",
        "code": """```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

data = [38, 27, 43, 3, 9, 82, 10]
print("Sorted:", merge_sort(data))
```"""
    },
    {
        "id": "py_fibonacci",
        "languages": ["python"],
        "keywords": ["fibonacci", "fibonacci dp", "fibonacci memoization", "fibonacci sequence"],
        "title": "Fibonacci Sequence (Memoization & O(1) Space Iterative)",
        "description": "Computes the Nth Fibonacci number using linear memoization and constant space iteration.",
        "code": """```python
def fibonacci_iterative(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr

memo = {}
def fibonacci_memo(n: int) -> int:
    if n in memo:
        return memo[n]
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    memo[n] = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    return memo[n]

for i in range(12):
    print(f"Fib({i}) = {fibonacci_iterative(i)}")
```"""
    },
    {
        "id": "js_promise_all",
        "languages": ["javascript", "typescript"],
        "keywords": ["promise all", "implement promise all", "promise all scratch", "promise all javascript"],
        "title": "Promise.all Implementation from Scratch (JavaScript)",
        "description": "Resolves when all promises resolve, or rejects immediately upon the first rejected promise.",
        "code": """```javascript
function promiseAll(promises) {
    return new Promise((resolve, reject) => {
        if (!Array.isArray(promises)) {
            return reject(new TypeError("Argument must be an array"));
        }
        if (promises.length === 0) {
            return resolve([]);
        }
        const results = new Array(promises.length);
        let completed = 0;

        promises.forEach((p, index) => {
            Promise.resolve(p).then(value => {
                results[index] = value;
                completed += 1;
                if (completed === promises.length) {
                    resolve(results);
                }
            }).catch(err => {
                reject(err);
            });
        });
    });
}

const p1 = Promise.resolve(42);
const p2 = new Promise(resolve => setTimeout(() => resolve("Nexus"), 100));
const p3 = Promise.resolve(true);

promiseAll([p1, p2, p3]).then(values => {
    console.log("All resolved:", values);
});
```"""
    },
    {
        "id": "c_quicksort",
        "languages": ["c"],
        "keywords": ["quicksort in c", "c quicksort", "quicksort algorithm c"],
        "title": "In-Place Quicksort Algorithm in Pure C",
        "description": "Standard Lomuto partition scheme sorting an integer array in-place.",
        "code": """```c
#include <stdio.h>

void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void quicksort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

int main() {
    int arr[] = {10, 7, 8, 9, 1, 5};
    int n = sizeof(arr) / sizeof(arr[0]);
    quicksort(arr, 0, n - 1);
    printf("Sorted array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\\n");
    return 0;
}
```"""
    },
    {
        "id": "c_binary_search",
        "languages": ["c"],
        "keywords": ["binary search c", "c binary search", "bsearch in c"],
        "title": "Binary Search Algorithm in Pure C",
        "description": "Searches for an element in a sorted integer array with logarithmic time complexity.",
        "code": """```c
#include <stdio.h>

int binarySearch(int arr[], int size, int target) {
    int low = 0;
    int high = size - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int main() {
    int data[] = {3, 9, 14, 19, 25, 31, 42, 55, 68, 77, 89};
    int size = sizeof(data) / sizeof(data[0]);
    int target = 42;
    int index = binarySearch(data, size, target);
    if (index != -1) {
        printf("Found %d at index %d\\n", target, index);
    } else {
        printf("Element not found\\n");
    }
    return 0;
}
```"""
    },
    {
        "id": "rust_binary_search",
        "languages": ["rust"],
        "keywords": ["rust binary search", "binary search rust", "bsearch rust"],
        "title": "Binary Search in Rust (Idiomatic & Safe)",
        "description": "Safe logarithmic search over sorted slices returning Option<usize>.",
        "code": """```rust
pub fn binary_search<T: Ord>(arr: &[T], target: &T) -> Option<usize> {
    let mut low = 0;
    let mut high = arr.len();

    while low < high {
        let mid = low + (high - low) / 2;
        match arr[mid].cmp(target) {
            std::cmp::Ordering::Equal => return Some(mid),
            std::cmp::Ordering::Less => low = mid + 1,
            std::cmp::Ordering::Greater => high = mid,
        }
    }
    None
}

fn main() {
    let numbers = vec![2, 4, 6, 8, 10, 12, 14, 16, 18, 20];
    let target = 14;
    match binary_search(&numbers, &target) {
        Some(idx) => println!("Target {} found at index {}", target, idx),
        None => println!("Target {} not found", target),
    }
}
```"""
    },
    {
        "id": "java_singleton",
        "languages": ["java"],
        "keywords": ["java singleton", "singleton pattern java", "double checked locking singleton"],
        "title": "Thread-Safe Singleton with Double-Checked Locking (Java)",
        "description": "Guarantees a single instance with lazy initialization and volatile memory barriers.",
        "code": """```java
public class NexusManager {
    private static volatile NexusManager instance;
    private final String systemId;

    private NexusManager() {
        this.systemId = "NEXUS-226-OFFLINE";
    }

    public static NexusManager getInstance() {
        if (instance == null) {
            synchronized (NexusManager.class) {
                if (instance == null) {
                    instance = new NexusManager();
                }
            }
        }
        return instance;
    }

    public String getSystemId() {
        return this.systemId;
    }

    public static void main(String[] args) {
        NexusManager s1 = NexusManager.getInstance();
        NexusManager s2 = NexusManager.getInstance();
        System.out.println("Same instance: " + (s1 == s2));
        System.out.println("System ID: " + s1.getSystemId());
    }
}
```"""
    },
    {
        "id": "sql_top_n_per_group",
        "languages": ["sql"],
        "keywords": ["top n per group", "top salaries department", "top records group", "dense_rank partition by"],
        "title": "Top N Records Per Group (SQL DENSE_RANK Window Function)",
        "description": "Finds the top 3 highest earning employees in each department using window partition ranking.",
        "code": """```sql
WITH RankedSalaries AS (
    SELECT 
        d.name AS Department,
        e.name AS Employee,
        e.salary AS Salary,
        DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS rnk
    FROM Employee e
    JOIN Department d ON e.department_id = d.id
)
SELECT Department, Employee, Salary
FROM RankedSalaries
WHERE rnk <= 3
ORDER BY Department, Salary DESC;
```"""
    },
    {
        "id": "py_dijkstra",
        "languages": ["python"],
        "keywords": ["dijkstra", "dijkstras algorithm", "shortest path", "weighted graph shortest path", "priority queue dijkstra", "min heap graph", "find shortest path"],
        "title": "Dijkstra's Shortest Path Algorithm (Priority Queue O((V + E) log V))",
        "description": "Calculates the shortest paths from a start vertex to all other vertices in a weighted graph with non-negative edge weights using a min-heap.",
        "code": """```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    predecessors = {node: None for node in graph}

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node]:
            continue
        for neighbor, weight in graph[curr_node]:
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = curr_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, predecessors

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2)]
}

distances, predecessors = dijkstra(graph, 'A')
for node, d in distances.items():
    print(f"Shortest path from A to {node}: {d}")
```"""
    },
    {
        "id": "py_trie",
        "languages": ["python"],
        "keywords": ["trie", "prefix tree", "trie insert search", "trie implementation", "prefix search", "autocomplete trie"],
        "title": "Trie (Prefix Tree) Implementation",
        "description": "Efficient retrieval tree data structure for string insertion, exact search, and prefix matching in O(L) time.",
        "code": """```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end_of_word = True

    def search(self, word: str) -> bool:
        curr = self.root
        for char in word:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return curr.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return True

trie = Trie()
for word in ["apple", "app", "application", "apt"]:
    trie.insert(word)

print("Search 'apple':", trie.search("apple"))
print("Search 'app':", trie.search("app"))
print("Search 'appl':", trie.search("appl"))
print("Starts with 'ap':", trie.starts_with("ap"))
```"""
    },
    {
        "id": "py_longest_substring",
        "languages": ["python"],
        "keywords": ["longest substring without repeating characters", "longest substring", "sliding window substring", "unique characters substring", "longest non repeating substring"],
        "title": "Longest Substring Without Repeating Characters (Sliding Window O(n))",
        "description": "Calculates the maximum length of a substring with all distinct characters using a dynamic sliding window and character index hash map.",
        "code": """```python
def length_of_longest_substring(s: str) -> int:
    char_map = {}
    max_len = 0
    left = 0
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        curr_len = right - left + 1
        if curr_len > max_len:
            max_len = curr_len
    return max_len

test_cases = ["abcabcbb", "bbbbb", "pwwkew", ""]
for s in test_cases:
    print(f"'{s}' -> {length_of_longest_substring(s)}")
```"""
    },
    {
        "id": "py_coin_change",
        "languages": ["python"],
        "keywords": ["coin change", "coin change problem", "coin change dynamic programming", "min coins", "minimum coins dp", "coin change leetcode"],
        "title": "Coin Change Problem (Bottom-Up Dynamic Programming O(amount * n))",
        "description": "Computes the fewest number of coins needed to make up a target amount using bottom-up tabulation.",
        "code": """```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

coins = [1, 2, 5]
amount = 11
print(f"Fewest coins to make {amount} with {coins}: {coin_change(coins, amount)}")
```"""
    },
    {
        "id": "py_merge_intervals",
        "languages": ["python"],
        "keywords": ["merge intervals", "overlapping intervals", "interval merge", "merge interval leetcode", "merge overlapping intervals"],
        "title": "Merge Overlapping Intervals (O(n log n) Sort & Merge)",
        "description": "Sorts intervals by start time and merges all overlapping or adjacent ranges into a minimal list of disjoint intervals.",
        "code": """```python
def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))
    return merged

intervals = [(1, 3), (2, 6), (8, 10), (15, 18)]
print("Original:", intervals)
print("Merged:", merge_intervals(intervals))
```"""
    },
    {
        "id": "py_word_search",
        "languages": ["python"],
        "keywords": ["word search", "word search backtracking", "grid word search", "2d grid word search", "boggle search", "word search leetcode"],
        "title": "Word Search on 2D Grid (Backtracking DFS)",
        "description": "Searches for a word in a 2D character matrix using depth-first search backtracking with in-place cell marking.",
        "code": """```python
def exist(board, word):
    rows = len(board)
    cols = len(board[0])

    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False
        temp = board[r][c]
        board[r][c] = '#'
        found = (
            dfs(r + 1, c, idx + 1) or
            dfs(r - 1, c, idx + 1) or
            dfs(r, c + 1, idx + 1) or
            dfs(r, c - 1, idx + 1)
        )
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False

board = [
    ['A', 'B', 'C', 'E'],
    ['S', 'F', 'C', 'S'],
    ['A', 'D', 'E', 'E']
]
print("Word 'ABCCED':", exist(board, "ABCCED"))
print("Word 'SEE':", exist(board, "SEE"))
print("Word 'ABCB':", exist(board, "ABCB"))
```"""
    },
    {
        "id": "py_binary_tree_level_order",
        "languages": ["python"],
        "keywords": ["level order traversal", "binary tree level order", "bfs binary tree", "tree breadth first search", "tree level order"],
        "title": "Binary Tree Level Order Traversal (BFS O(n))",
        "description": "Traverses a binary tree level-by-level using a double-ended queue, returning values grouped by tree depth.",
        "code": """```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(current_level)
    return result

root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
print("Level order traversal:", level_order(root))
```"""
    },
    {
        "id": "py_topological_sort",
        "languages": ["python"],
        "keywords": ["topological sort", "topological sorting", "kahn algorithm", "dag topological sort", "course schedule", "graph topological sort"],
        "title": "Topological Sort (Kahn's In-Degree BFS Algorithm)",
        "description": "Determines a valid linear execution order for dependencies in a Directed Acyclic Graph (DAG) or detects cycles.",
        "code": """```python
from collections import deque, defaultdict

def topological_sort(num_nodes, edges):
    adj = defaultdict(list)
    in_degree = [0] * num_nodes
    for src, dst in edges:
        adj[src].append(dst)
        in_degree[dst] += 1

    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(order) == num_nodes:
        return order
    return []

edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
print("Topological order:", topological_sort(6, edges))
```"""
    },
    {
        "id": "py_file_io_safe",
        "languages": ["python"],
        "keywords": ["open file in python", "read file in python", "write file in python", "file io in python", "safe file read python", "how to read a file in python", "how to open file in python"],
        "title": "Safe File I/O in Python (Atomic Write & Context Manager)",
        "description": "Production-grade pattern for reading, writing, and parsing files safely using context managers, atomic swaps, and UTF-8 encoding.",
        "code": """```python
import os
import json

def safe_write_json(file_path: str, data: dict) -> bool:
    try:
        temp_path = f"{file_path}.tmp"
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, file_path)
        return True
    except Exception as e:
        print(f"File write error: {e}")
        return False

def safe_read_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        return ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"File read error: {e}")
        return ""

test_file = "demo_file.json"
safe_write_json(test_file, {"status": "ok", "entries": [1, 2, 3]})
print("Read content:", safe_read_file(test_file))
```"""
    },
    {
        "id": "py_thread_pool_executor",
        "languages": ["python"],
        "keywords": ["thread pool python", "threadpoolexecutor", "concurrent futures python", "multi threading python", "parallel tasks python", "run threads python"],
        "title": "ThreadPoolExecutor Concurrent Worker Pattern (Python)",
        "description": "Manages parallel execution of I/O-bound tasks using concurrent.futures with task submission, exception trapping, and result aggregation.",
        "code": """```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_item(item_id: int, payload: str) -> dict:
    time.sleep(0.02)
    return {"id": item_id, "processed": payload.upper()}

items = [(i, f"payload_{i}") for i in range(5)]
results = []

with ThreadPoolExecutor(max_workers=4) as executor:
    future_to_id = {executor.submit(process_item, it[0], it[1]): it[0] for it in items}
    for future in as_completed(future_to_id):
        item_id = future_to_id[future]
        try:
            res = future.result()
            results.append(res)
        except Exception as exc:
            print(f"Item {item_id} generated an exception: {exc}")

for res in sorted(results, key=lambda x: x["id"]):
    print("Result:", res)
```"""
    },
    {
        "id": "py_decorator_cache",
        "languages": ["python"],
        "keywords": ["python decorator", "memoize decorator", "cache decorator", "custom decorator python", "function decorator", "timer decorator"],
        "title": "Custom Decorators for Memoization & Performance Timing (Python)",
        "description": "Production decorators utilizing functools.wraps to implement transparent in-memory result caching and sub-millisecond execution timing.",
        "code": """```python
import functools
import time

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        print(f"[{func.__name__}] finished in {elapsed_ms:.3f} ms")
        return result
    return wrapper

@timer
@memoize
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print("fib(30) =", fib(30))
```"""
    },
    {
        "id": "py_fastapi_rest_api",
        "languages": ["python"],
        "keywords": ["fastapi rest api", "fastapi template", "rest api python", "fastapi crud", "create api python", "how to make api in python"],
        "title": "FastAPI Production REST API Template",
        "description": "Complete production FastAPI application structure featuring Pydantic schemas, CRUD path operations, status codes, and HTTP exception handling.",
        "code": """```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Offline High Performance API", version="1.0.0")

class Item(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0.0)

db: List[Item] = []

@app.get("/items", response_model=List[Item])
def get_all_items():
    return db

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    item.id = len(db) + 1
    db.append(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
def get_item_by_id(item_id: int):
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
```"""
    },
    {
        "id": "js_custom_promise",
        "languages": ["javascript", "typescript"],
        "keywords": ["custom promise javascript", "promise implementation", "promise from scratch", "how promise works js", "implement promise in javascript"],
        "title": "Custom Promise Implementation (Promises/A+ Compliant Core)",
        "description": "Constructs a Promise class from scratch supporting asynchronous state transitions, microtask queue dispatch, and fluent .then()/.catch() chaining.",
        "code": """```javascript
class MyPromise {
  constructor(executor) {
    this.state = 'PENDING';
    this.value = undefined;
    this.handlers = [];

    const resolve = (val) => {
      if (this.state !== 'PENDING') return;
      this.state = 'FULFILLED';
      this.value = val;
      this.handlers.forEach(h => h.onFulfilled(val));
    };

    const reject = (err) => {
      if (this.state !== 'PENDING') return;
      this.state = 'REJECTED';
      this.value = err;
      this.handlers.forEach(h => h.onRejected(err));
    };

    try {
      executor(resolve, reject);
    } catch (err) {
      reject(err);
    }
  }

  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      const handle = () => {
        try {
          if (this.state === 'FULFILLED') {
            const res = onFulfilled ? onFulfilled(this.value) : this.value;
            resolve(res);
          } else if (this.state === 'REJECTED') {
            const res = onRejected ? onRejected(this.value) : this.value;
            resolve(res);
          }
        } catch (err) {
          reject(err);
        }
      };

      if (this.state === 'PENDING') {
        this.handlers.push({
          onFulfilled: () => handle(),
          onRejected: () => handle()
        });
      } else {
        queueMicrotask(handle);
      }
    });
  }
}

const p = new MyPromise((res) => setTimeout(() => res('Async Resolved!'), 50));
p.then(val => console.log('Promise Output:', val));
```"""
    },
    {
        "id": "js_deep_flatten",
        "languages": ["javascript", "typescript"],
        "keywords": ["deep flatten javascript", "flatten array js", "flat array generator", "flatten nested array", "deep flatten array"],
        "title": "Deep Flatten Array (Iterative Stack & ES6 Generator)",
        "description": "Flattens arbitrarily nested multi-dimensional arrays without recursion call-stack overflow limits using ES6 generators and an explicit stack.",
        "code": """```javascript
function* flatGenerator(arr) {
  for (const item of arr) {
    if (Array.isArray(item)) {
      yield* flatGenerator(item);
    } else {
      yield item;
    }
  }
}

function deepFlattenIterative(arr) {
  const stack = [...arr];
  const res = [];
  while (stack.length) {
    const next = stack.pop();
    if (Array.isArray(next)) {
      stack.push(...next);
    } else {
      res.push(next);
    }
  }
  return res.reverse();
}

const nested = [1, [2, [3, [4, [5]]]], 6];
console.log("Generator result:", [...flatGenerator(nested)]);
console.log("Iterative result:", deepFlattenIterative(nested));
```"""
    },
    {
        "id": "js_react_use_debounce",
        "languages": ["typescript", "javascript"],
        "keywords": ["react custom hook", "usedebounce hook", "uselocalstorage react", "react hooks typescript", "custom hook typescript"],
        "title": "React Custom Hooks: useDebounce & useLocalStorage",
        "description": "Typed React custom hooks for delayed input synchronization (useDebounce) and reactive browser storage synchronization (useLocalStorage).",
        "code": """```typescript
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delayMs: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delayMs);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delayMs]);

  return debouncedValue;
}

export function useLocalStorage<T>(key: string, initialValue: T): [T, (val: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (err) {
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (err) {
      console.error(err);
    }
  };

  return [storedValue, setValue];
}
```"""
    },
    {
        "id": "js_state_store",
        "languages": ["javascript", "typescript"],
        "keywords": ["state store javascript", "redux from scratch", "pub sub state", "state management javascript", "mini redux"],
        "title": "State Store Implementation (Pub/Sub State Management)",
        "description": "Complete predictable state container implementation featuring action dispatching, pure reducer state updates, and subscriber subscription management.",
        "code": """```javascript
function createStore(reducer, initialState) {
  let state = initialState;
  const listeners = new Set();

  return {
    getState: () => state,
    dispatch: (action) => {
      state = reducer(state, action);
      listeners.forEach(fn => fn(state));
    },
    subscribe: (listener) => {
      listeners.add(listener);
      return () => listeners.delete(listener);
    }
  };
}

const counterReducer = (state = { count: 0 }, action) => {
  switch (action.type) {
    case 'INC': return { ...state, count: state.count + 1 };
    case 'DEC': return { ...state, count: state.count - 1 };
    default: return state;
  }
};

const store = createStore(counterReducer, { count: 0 });
const unsubscribe = store.subscribe(s => console.log("State:", s));
store.dispatch({ type: 'INC' });
store.dispatch({ type: 'INC' });
unsubscribe();
```"""
    },
    {
        "id": "js_fetch_with_retry",
        "languages": ["javascript", "typescript"],
        "keywords": ["fetch with retry", "retry fetch javascript", "fetch timeout backoff", "resilient http request js", "fetch retry exponential backoff"],
        "title": "Resilient HTTP Fetch with Exponential Backoff & Timeout",
        "description": "Production fetch wrapper featuring configurable retries, exponential jittered backoff, and AbortController request timeouts.",
        "code": """```javascript
async function fetchWithRetry(url, options = {}, retries = 3, backoffMs = 250) {
  const timeoutMs = options.timeout || 6000;
  for (let attempt = 0; attempt <= retries; attempt++) {
    const controller = new AbortController();
    const timerId = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await fetch(url, { ...options, signal: controller.signal });
      clearTimeout(timerId);
      if (!response.ok && attempt < retries) {
        throw new Error(`HTTP ${response.status}`);
      }
      return response;
    } catch (err) {
      clearTimeout(timerId);
      if (attempt === retries) throw err;
      const delay = backoffMs * Math.pow(2, attempt) + Math.random() * 50;
      await new Promise(r => setTimeout(r, delay));
    }
  }
}
```"""
    },
    {
        "id": "cpp_unique_ptr",
        "languages": ["cpp"],
        "keywords": ["unique ptr cpp", "smart pointer cpp", "raii pointer cpp", "custom unique ptr", "move semantics pointer"],
        "title": "RAII Smart Pointer Implementation (UniquePtr in C++)",
        "description": "Implements an exclusive-ownership smart pointer from scratch with explicit move semantics, deleted copy constructor, and RAII automatic deallocation.",
        "code": """```cpp
#include <iostream>
#include <utility>

template <typename T>
class UniquePtr {
private:
    T* ptr;
public:
    explicit UniquePtr(T* p = nullptr) : ptr(p) {}
    ~UniquePtr() { delete ptr; }

    UniquePtr(const UniquePtr&) = delete;
    UniquePtr& operator=(const UniquePtr&) = delete;

    UniquePtr(UniquePtr&& other) noexcept : ptr(other.ptr) {
        other.ptr = nullptr;
    }

    UniquePtr& operator=(UniquePtr&& other) noexcept {
        if (this != &other) {
            delete ptr;
            ptr = other.ptr;
            other.ptr = nullptr;
        }
        return *this;
    }

    T& operator*() const { return *ptr; }
    T* operator->() const { return ptr; }
    T* get() const { return ptr; }
};

int main() {
    UniquePtr<int> val(new int(100));
    std::cout << "Value: " << *val << std::endl;
    UniquePtr<int> moved = std::move(val);
    std::cout << "Moved: " << *moved << std::endl;
    return 0;
}
```"""
    },
    {
        "id": "cpp_circular_buffer",
        "languages": ["cpp"],
        "keywords": ["circular buffer cpp", "ring buffer cpp", "thread safe circular buffer", "bounded queue cpp", "circular queue cpp"],
        "title": "Thread-Safe Circular Ring Buffer (C++)",
        "description": "Fixed-capacity circular FIFO buffer synchronized across multiple producers and consumers using std::mutex and std::condition_variable.",
        "code": """```cpp
#include <vector>
#include <mutex>
#include <condition_variable>
#include <iostream>

template <typename T>
class CircularBuffer {
private:
    std::vector<T> buf;
    size_t head = 0;
    size_t tail = 0;
    size_t max_size;
    bool full = false;
    mutable std::mutex mtx;
    std::condition_variable not_full;
    std::condition_variable not_empty;

public:
    explicit CircularBuffer(size_t size) : buf(size), max_size(size) {}

    void push(T item) {
        std::unique_lock<std::mutex> lock(mtx);
        not_full.wait(lock, [this]() { return !full; });
        buf[head] = item;
        head = (head + 1) % max_size;
        full = (head == tail);
        not_empty.notify_one();
    }

    T pop() {
        std::unique_lock<std::mutex> lock(mtx);
        not_empty.wait(lock, [this]() { return full || (head != tail); });
        T val = buf[tail];
        full = false;
        tail = (tail + 1) % max_size;
        not_full.notify_one();
        return val;
    }
};

int main() {
    CircularBuffer<int> cb(3);
    cb.push(10);
    cb.push(20);
    std::cout << "Popped: " << cb.pop() << std::endl;
    std::cout << "Popped: " << cb.pop() << std::endl;
    return 0;
}
```"""
    },
    {
        "id": "cpp_meyers_singleton",
        "languages": ["cpp"],
        "keywords": ["singleton cpp", "meyers singleton", "thread safe singleton cpp", "singleton pattern c++", "singleton in c++"],
        "title": "Meyers Thread-Safe Singleton Pattern (C++)",
        "description": "Thread-safe, lazy-initialized Singleton relying on C++11 static local variable initialization semantics.",
        "code": """```cpp
#include <iostream>
#include <string>

class Singleton {
public:
    static Singleton& getInstance() {
        static Singleton instance;
        return instance;
    }

    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

    void log(const std::string& msg) {
        std::cout << "[System Log] " << msg << std::endl;
    }

private:
    Singleton() {
        std::cout << "Singleton instance initialized." << std::endl;
    }
    ~Singleton() = default;
};

int main() {
    Singleton::getInstance().log("Thread safe access verified.");
    return 0;
}
```"""
    },
    {
        "id": "cpp_matrix_multiply",
        "languages": ["cpp"],
        "keywords": ["matrix multiplication cpp", "cache friendly matrix multiply", "matrix multiply c++", "matrix dot product", "multiply matrix cpp"],
        "title": "Cache-Friendly 2D Matrix Multiplication (C++)",
        "description": "High-speed matrix multiplication employing inner loop interchange (i-k-j) to optimize CPU L1/L2 cache locality.",
        "code": """```cpp
#include <vector>
#include <iostream>

std::vector<std::vector<double>> multiply_matrices(
    const std::vector<std::vector<double>>& A,
    const std::vector<std::vector<double>>& B
) {
    size_t n = A.size();
    size_t m = A[0].size();
    size_t p = B[0].size();
    std::vector<std::vector<double>> C(n, std::vector<double>(p, 0.0));

    for (size_t i = 0; i < n; ++i) {
        for (size_t k = 0; k < m; ++k) {
            double r = A[i][k];
            for (size_t j = 0; j < p; ++j) {
                C[i][j] += r * B[k][j];
            }
        }
    }
    return C;
}

int main() {
    std::vector<std::vector<double>> A = {{1, 2}, {3, 4}};
    std::vector<std::vector<double>> B = {{5, 6}, {7, 8}};
    auto C = multiply_matrices(A, B);
    std::cout << "C[0][0]: " << C[0][0] << ", C[1][1]: " << C[1][1] << std::endl;
    return 0;
}
```"""
    },
    {
        "id": "rust_custom_error",
        "languages": ["rust"],
        "keywords": ["custom error rust", "error handling rust", "rust std error", "thiserror rust", "rust result error", "custom error enum rust"],
        "title": "Custom Error Handling in Rust (Display & std::error::Error)",
        "description": "Idiomatic domain error enum implementing std::fmt::Display and std::error::Error traits with source error unboxing.",
        "code": """```rust
use std::fmt;
use std::error::Error;

#[derive(Debug)]
pub enum AppError {
    NotFound(String),
    InvalidInput(String),
    Io(std::io::Error),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::NotFound(item) => write!(f, "Entity not found: {}", item),
            AppError::InvalidInput(msg) => write!(f, "Invalid input: {}", msg),
            AppError::Io(e) => write!(f, "I/O failure: {}", e),
        }
    }
}

impl Error for AppError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            AppError::Io(ref e) => Some(e),
            _ => None,
        }
    }
}

fn validate_positive(val: i32) -> Result<i32, AppError> {
    if val <= 0 {
        Err(AppError::InvalidInput("Value must be positive".to_string()))
    } else {
        Ok(val * 2)
    }
}

fn main() {
    match validate_positive(-10) {
        Ok(v) => println!("Success: {}", v),
        Err(e) => eprintln!("Encountered error: {}", e),
    }
}
```"""
    },
    {
        "id": "rust_thread_channel",
        "languages": ["rust"],
        "keywords": ["rust concurrency channel", "rust mpsc", "rust producer consumer", "rust threads arc mutex", "channels in rust"],
        "title": "Multi-Threaded Producer-Consumer with Channels (Rust)",
        "description": "Concurrent worker pattern using std::sync::mpsc multi-producer single-consumer channels and Arc<Mutex<T>> thread-safe state.",
        "code": """```rust
use std::sync::{mpsc, Arc, Mutex};
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    let counter = Arc::new(Mutex::new(0));

    let mut handles = vec![];
    for id in 0..4 {
        let thread_tx = tx.clone();
        let thread_counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = thread_counter.lock().unwrap();
            *num += 1;
            thread_tx.send(format!("Worker {} completed step {}", id, *num)).unwrap();
        });
        handles.push(handle);
    }
    drop(tx);

    for msg in rx {
        println!("{}", msg);
    }

    for h in handles {
        h.join().unwrap();
    }
}
```"""
    },
    {
        "id": "rust_custom_iterator",
        "languages": ["rust"],
        "keywords": ["rust custom iterator", "rust iterator trait", "iterator next rust", "rust lazy iterator", "implement iterator rust"],
        "title": "Custom Iterator Implementation in Rust",
        "description": "Implements the core Iterator trait with next() returning Option<Self::Item> for lazy sequence evaluation.",
        "code": """```rust
struct CollatzSequence {
    current: u64,
}

impl CollatzSequence {
    fn new(start: u64) -> Self {
        CollatzSequence { current: start }
    }
}

impl Iterator for CollatzSequence {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current == 0 {
            return None;
        }
        let val = self.current;
        if self.current == 1 {
            self.current = 0;
        } else if self.current % 2 == 0 {
            self.current /= 2;
        } else {
            self.current = self.current * 3 + 1;
        }
        Some(val)
    }
}

fn main() {
    let sequence: Vec<u64> = CollatzSequence::new(6).collect();
    println!("Collatz sequence: {:?}", sequence);
}
```"""
    },
    {
        "id": "go_graceful_shutdown",
        "languages": ["golang"],
        "keywords": ["go graceful shutdown", "golang http server shutdown", "graceful shutdown golang", "context timeout go", "graceful shutdown go"],
        "title": "Go HTTP Server with Graceful Shutdown",
        "description": "Production HTTP server setup with OS signal notification, context cancellation, and active connection drain timeout.",
        "code": """```go
package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"online"}`))
	})

	server := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			fmt.Printf("Listen error: %v\n", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		fmt.Printf("Forced shutdown: %v\n", err)
	}
	fmt.Println("Server exited cleanly.")
}
```"""
    },
    {
        "id": "go_pipeline_channels",
        "languages": ["golang"],
        "keywords": ["go pipeline channels", "golang concurrency pipeline", "channel pipeline go", "goroutine streaming", "channels pipeline go"],
        "title": "Go Concurrency Pipeline with Channels",
        "description": "Data transformation pipeline linking goroutines through typed channels with explicit channel closing semantics.",
        "code": """```go
package main

import "fmt"

func generator(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		for _, n := range nums {
			out <- n
		}
		close(out)
	}()
	return out
}

func square(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for n := range in {
			out <- n * n
		}
		close(out)
	}()
	return out
}

func main() {
	in := generator(1, 2, 3, 4, 5)
	out := square(in)
	for val := range out {
		fmt.Printf("%d ", val)
	}
	fmt.Println()
}
```"""
    },
    {
        "id": "go_sync_cache",
        "languages": ["golang"],
        "keywords": ["go thread safe cache", "golang sync rwmutex cache", "go in memory cache", "cache with ttl go", "concurrency safe cache go"],
        "title": "Thread-Safe In-Memory Cache in Go (sync.RWMutex)",
        "description": "Concurrent key-value cache implementation supporting TTL expiration and fine-grained reader/writer mutex locking.",
        "code": """```go
package main

import (
	"sync"
	"time"
)

type CacheItem struct {
	value      interface{}
	expiration int64
}

type SafeCache struct {
	items map[string]CacheItem
	mutex sync.RWMutex
}

func NewSafeCache() *SafeCache {
	return &SafeCache{
		items: make(map[string]CacheItem),
	}
}

func (c *SafeCache) Set(key string, value interface{}, ttl time.Duration) {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	c.items[key] = CacheItem{
		value:      value,
		expiration: time.Now().Add(ttl).UnixNano(),
	}
}

func (c *SafeCache) Get(key string) (interface{}, bool) {
	c.mutex.RLock()
	defer c.mutex.RUnlock()
	item, found := c.items[key]
	if !found {
		return nil, false
	}
	if time.Now().UnixNano() > item.expiration {
		return nil, false
	}
	return item.value, true
}
```"""
    },
    {
        "id": "sql_consecutive_numbers",
        "languages": ["sql"],
        "keywords": ["consecutive numbers sql", "find consecutive numbers", "sql window consecutive", "lead lag sql consecutive", "consecutive entries sql"],
        "title": "SQL: Consecutive Numbers Query",
        "description": "Identifies numbers appearing at least 3 consecutive times in a sequence table using the LEAD() window function.",
        "code": """```sql
WITH SequencedLogs AS (
    SELECT 
        num,
        LEAD(num, 1) OVER (ORDER BY id) AS next_num,
        LEAD(num, 2) OVER (ORDER BY id) AS next_next_num
    FROM Logs
)
SELECT DISTINCT num AS ConsecutiveNums
FROM SequencedLogs
WHERE num = next_num AND num = next_next_num;
```"""
    },
    {
        "id": "sql_running_total",
        "languages": ["sql"],
        "keywords": ["running total sql", "cumulative sum sql", "sum over order by", "sql running balance", "cumulative total sql"],
        "title": "SQL: Running Total / Cumulative Sum",
        "description": "Calculates running cumulative total partitioned by account using window frame specifications.",
        "code": """```sql
SELECT 
    transaction_date,
    account_id,
    amount,
    SUM(amount) OVER (
        PARTITION BY account_id 
        ORDER BY transaction_date, id 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM transactions
ORDER BY account_id, transaction_date;
```"""
    },
    {
        "id": "sql_recursive_cte",
        "languages": ["sql"],
        "keywords": ["recursive cte sql", "hierarchical query sql", "employee manager hierarchy", "recursive common table expression", "tree query sql"],
        "title": "SQL: Recursive CTE for Hierarchical Organization Trees",
        "description": "Recursively traverses a manager-employee hierarchy tree, constructing depth levels and hierarchical path strings.",
        "code": """```sql
WITH RECURSIVE OrgHierarchy AS (
    SELECT 
        id,
        name,
        manager_id,
        1 AS level,
        CAST(name AS VARCHAR(1000)) AS reporting_chain
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT 
        e.id,
        e.name,
        e.manager_id,
        h.level + 1,
        CAST(h.reporting_chain || ' -> ' || e.name AS VARCHAR(1000))
    FROM employees e
    JOIN OrgHierarchy h ON e.manager_id = h.id
)
SELECT id, name, manager_id, level, reporting_chain
FROM OrgHierarchy
ORDER BY level, manager_id;
```"""
    },
    {
        "id": "java_producer_consumer",
        "languages": ["java"],
        "keywords": ["producer consumer java", "blockingqueue java", "concurrent queue java", "multithreading java producer consumer", "producer consumer pattern java"],
        "title": "Java: Thread-Safe Producer-Consumer with BlockingQueue",
        "description": "Concurrent Producer-Consumer coordination utilizing ArrayBlockingQueue with thread management via ExecutorService.",
        "code": """```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ProducerConsumerDemo {
    public static void main(String[] args) {
        BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(10);
        ExecutorService executor = Executors.newFixedThreadPool(2);

        Runnable producer = () -> {
            try {
                for (int i = 1; i <= 5; i++) {
                    queue.put(i);
                    System.out.println("Produced: " + i);
                    Thread.sleep(80);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        };

        Runnable consumer = () -> {
            try {
                for (int i = 1; i <= 5; i++) {
                    int val = queue.take();
                    System.out.println("Consumed: " + val);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        };

        executor.submit(producer);
        executor.submit(consumer);
        executor.shutdown();
    }
}
```"""
    },
    {
        "id": "csharp_repository_pattern",
        "languages": ["csharp"],
        "keywords": ["repository pattern c#", "csharp generic repository", "irepository c#", "async repository csharp", "generic repository pattern c#"],
        "title": "C#: Generic Async Repository Pattern",
        "description": "Clean architecture repository abstraction with generic type constraints, async Task methods, and LINQ expression predicates.",
        "code": """```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Threading.Tasks;

public interface IRepository<T> where T : class
{
    Task<T> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate);
    Task AddAsync(T entity);
    void Remove(T entity);
}

public class InMemoryRepository<T> : IRepository<T> where T : class
{
    private readonly List<T> _entities = new List<T>();

    public Task<T> GetByIdAsync(int id) => Task.FromResult(_entities.FirstOrDefault());
    public Task<IEnumerable<T>> GetAllAsync() => Task.FromResult<IEnumerable<T>>(_entities);
    public Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate) =>
        Task.FromResult<IEnumerable<T>>(_entities.AsQueryable().Where(predicate).ToList());
    public Task AddAsync(T entity)
    {
        _entities.Add(entity);
        return Task.CompletedTask;
    }
    public void Remove(T entity) => _entities.Remove(entity);
}
```"""
    },
    {
        "id": "bash_production_template",
        "languages": ["bash"],
        "keywords": ["bash script template", "production bash script", "bash error handling", "bash getopts script", "safe bash script", "bash script best practices"],
        "title": "Bash: Robust Production Script Template",
        "description": "Hardened shell script template featuring strict error flags (set -euo pipefail), signal cleanup traps, and CLI argument parsing.",
        "code": """```bash
set -euo pipefail
IFS=$'\n\t'

cleanup() {
    local exit_code=$?
    exit "${exit_code}"
}
trap cleanup EXIT INT TERM

log_info() {
    echo "[INFO] $(date +'%Y-%m-%d %H:%M:%S') - $*"
}

log_error() {
    echo "[ERROR] $(date +'%Y-%m-%d %H:%M:%S') - $*" >&2
}

VERBOSE=0
TARGET_DIR="."

while getopts "vd:h" opt; do
    case "${opt}" in
        v) VERBOSE=1 ;;
        d) TARGET_DIR="${OPTARG}" ;;
        h) echo "Usage: $0 [-v] [-d dir]"; exit 0 ;;
        *) echo "Invalid option"; exit 1 ;;
    esac
done

log_info "Executing pipeline on directory: ${TARGET_DIR}"
```"""
    },
    {
        "id": "html_css_responsive_navbar",
        "languages": ["html", "css"],
        "keywords": ["responsive navbar html css", "navbar html css", "navigation bar responsive", "mobile menu html css", "navbar template"],
        "title": "HTML & CSS: Responsive Navigation Bar",
        "description": "Modern responsive top navbar featuring flexbox auto-wrapping, subtle borders, and media query adaptation.",
        "code": """```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Navbar</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; }
    .navbar { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: #1e293b; border-bottom: 1px solid #334155; }
    .brand { font-size: 1.25rem; font-weight: 700; color: #38bdf8; text-decoration: none; }
    .nav-links { display: flex; gap: 1.5rem; list-style: none; }
    .nav-links a { color: #94a3b8; text-decoration: none; font-weight: 500; transition: color 0.2s; }
    .nav-links a:hover { color: #38bdf8; }
    @media (max-width: 640px) {
      .navbar { flex-direction: column; align-items: flex-start; gap: 1rem; }
      .nav-links { flex-direction: column; width: 100%; }
    }
  </style>
</head>
<body>
  <nav class="navbar">
    <a href="#" class="brand">Nexus System</a>
    <ul class="nav-links">
      <li><a href="#dashboard">Dashboard</a></li>
      <li><a href="#telemetry">Telemetry</a></li>
      <li><a href="#code">Code</a></li>
      <li><a href="#settings">Settings</a></li>
    </ul>
  </nav>
</body>
</html>
```"""
    },
{
        "id": "py_linked_list_cycle",
        "languages": ["python"],
        "keywords": ["linked list cycle", "detect cycle in linked list", "has cycle linked list", "floyd cycle detection", "tortoise and hare algorithm"],
        "title": "Detect Cycle in Linked List (Floyd's Tortoise & Hare O(n) Time, O(1) Space)",
        "description": "Determines whether a singly linked list contains a cycle using two pointers moving at different speeds.",
        "code": """```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head: ListNode) -> bool:
    if not head or not head.next:
        return False
    slow = head
    fast = head.next
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    return True

node1 = ListNode(3)
node2 = ListNode(2)
node3 = ListNode(0)
node4 = ListNode(-4)
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node2
print("Cycle detected:", has_cycle(node1))
```"""
    },
    {
        "id": "py_binary_search_tree",
        "languages": ["python"],
        "keywords": ["binary search tree", "bst implementation", "insert into bst", "search bst", "bst python"],
        "title": "Binary Search Tree (BST) Implementation with In-Order Traversal",
        "description": "Complete Binary Search Tree with node insertion, search, and sorted in-order traversal in O(log n) average time.",
        "code": """```python
class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if not self.root:
            self.root = BSTNode(val)
            return
        curr = self.root
        while True:
            if val < curr.val:
                if not curr.left:
                    curr.left = BSTNode(val)
                    break
                curr = curr.left
            else:
                if not curr.right:
                    curr.right = BSTNode(val)
                    break
                curr = curr.right

    def search(self, val) -> bool:
        curr = self.root
        while curr:
            if curr.val == val:
                return True
            curr = curr.left if val < curr.val else curr.right
        return False

    def in_order(self):
        res = []
        def traverse(node):
            if not node:
                return
            traverse(node.left)
            res.append(node.val)
            traverse(node.right)
        traverse(self.root)
        return res

bst = BinarySearchTree()
for num in [8, 3, 10, 1, 6, 14, 4, 7]:
    bst.insert(num)
print("In-order (sorted):", bst.in_order())
print("Search 6:", bst.search(6))
print("Search 15:", bst.search(15))
```"""
    },
    {
        "id": "py_longest_increasing_subsequence",
        "languages": ["python"],
        "keywords": ["longest increasing subsequence", "lis algorithm", "lis leetcode", "patience sorting", "lis bisect"],
        "title": "Longest Increasing Subsequence (Patience Sorting O(n log n))",
        "description": "Calculates the length of the longest strictly increasing subsequence using binary search (bisect) and patience sorting.",
        "code": """```python
import bisect

def length_of_lis(nums):
    tails = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)

nums = [10, 9, 2, 5, 3, 7, 101, 18]
print(f"Length of LIS for {nums}: {length_of_lis(nums)}")
```"""
    },
    {
        "id": "py_knapsack_01",
        "languages": ["python"],
        "keywords": ["0/1 knapsack", "knapsack problem", "knapsack dynamic programming", "knapsack python", "01 knapsack dp"],
        "title": "0/1 Knapsack Problem (Bottom-Up Dynamic Programming O(n * W))",
        "description": "Maximizes the total value of items that can fit into a knapsack of fixed capacity W using iterative dynamic programming.",
        "code": """```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]

weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]
capacity = 7
print(f"Maximum knapsack value (capacity {capacity}): {knapsack(weights, values, capacity)}")
```"""
    },
    {
        "id": "py_lcs",
        "languages": ["python"],
        "keywords": ["longest common subsequence", "lcs algorithm", "lcs dynamic programming", "lcs leetcode", "lcs python"],
        "title": "Longest Common Subsequence (2D Dynamic Programming O(m * n))",
        "description": "Finds the length of the longest subsequence present in both strings in the same relative order using dynamic programming.",
        "code": """```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    m = len(text1)
    n = len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

s1 = "abcde"
s2 = "ace"
print(f"LCS between '{s1}' and '{s2}': {longest_common_subsequence(s1, s2)}")
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
        clean = query.lower().strip().replace("c++", "cpp").replace("c#", "csharp")
        tokens = [t for t in _CODE_TOKEN_RE.findall(clean) if t not in _CODE_STOPWORDS]
        if not tokens:
            return None

        target_lang = None
        for tok in tokens:
            if tok in LANG_ALIASES:
                target_lang = LANG_ALIASES[tok]
                break

        matched_indices: Dict[int, int] = {}
        for idx, recipe in enumerate(self.recipes):
            kw_match = False
            for kw in recipe.get("keywords", []):
                if kw in clean:
                    matched_indices[idx] = matched_indices.get(idx, 0) + 25 + len(kw)
                    kw_match = True
                else:
                    kw_parts = [p for p in _CODE_TOKEN_RE.findall(kw.lower()) if p not in _CODE_STOPWORDS and len(p) > 2]
                    if len(kw_parts) >= 2 and all(p in tokens for p in kw_parts):
                        matched_indices[idx] = matched_indices.get(idx, 0) + 20 + sum(len(p) for p in kw_parts)
                        kw_match = True
            if kw_match:
                if target_lang:
                    if target_lang in recipe.get("languages", []):
                        matched_indices[idx] += 30
                    else:
                        matched_indices[idx] -= 25

        if matched_indices:
            best_idx = max(matched_indices.keys(), key=lambda i: matched_indices[i])
            if matched_indices[best_idx] >= 15:
                return self.recipes[best_idx]

        dyn = self._generate_dynamic_algorithm(query)
        if dyn:
            return dyn
        return None

    def _generate_dynamic_algorithm(self, query: str) -> Optional[Dict[str, Any]]:
        clean = query.lower().strip().replace("c++", "cpp").replace("c#", "csharp")
        tokens = set(_CODE_TOKEN_RE.findall(clean))
        target_lang = "python"
        for tok in tokens:
            if tok in LANG_ALIASES:
                target_lang = LANG_ALIASES[tok]
                break

        if "factorial" in clean:
            if target_lang == "python":
                return {
                    "id": "dyn_py_factorial",
                    "languages": ["python"],
                    "title": "Factorial Calculation (Iterative O(n) & Recursive)",
                    "description": "Calculates n! using iterative loop and recursive definition with edge-case validation.",
                    "code": """```python
def factorial_iterative(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def factorial_recursive(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

print("5! (iterative):", factorial_iterative(5))
print("5! (recursive):", factorial_recursive(5))
```"""
                }
            elif target_lang in ["cpp", "c"]:
                return {
                    "id": "dyn_cpp_factorial",
                    "languages": [target_lang],
                    "title": f"Factorial Calculation in {target_lang.upper()}",
                    "description": "Calculates factorial using an iterative loop with 64-bit unsigned integer.",
                    "code": f"""```{target_lang}
#include <iostream>

unsigned long long factorial(int n) {{
    if (n < 0) return 0;
    unsigned long long res = 1;
    for (int i = 2; i <= n; ++i) {{
        res *= i;
    }}
    return res;
}}

int main() {{
    std::cout << "5! = " << factorial(5) << std::endl;
    return 0;
}}
```"""
                }
            elif target_lang == "rust":
                return {
                    "id": "dyn_rust_factorial",
                    "languages": ["rust"],
                    "title": "Factorial Calculation in Rust",
                    "description": "Calculates factorial using functional iterator product folded over a range.",
                    "code": """```rust
fn factorial(n: u64) -> u64 {
    (1..=n).product()
}

fn main() {
    println!("5! = {}", factorial(5));
}
```"""
                }
            elif target_lang in ["javascript", "typescript"]:
                return {
                    "id": "dyn_js_factorial",
                    "languages": [target_lang],
                    "title": "Factorial Calculation in JavaScript",
                    "description": "Calculates factorial using an iterative loop and BigInt for arbitrary precision.",
                    "code": """```javascript
function factorial(n) {
  if (n < 0) throw new Error("Negative numbers unsupported");
  let res = 1n;
  for (let i = 2n; i <= BigInt(n); i++) {
    res *= i;
  }
  return res;
}

console.log("5! =", factorial(5).toString());
```"""
                }

        if any(w in clean for w in ["is prime", "prime check", "check prime", "prime number"]):
            if target_lang == "python":
                return {
                    "id": "dyn_py_prime",
                    "languages": ["python"],
                    "title": "Prime Number Verification (O(sqrt(n)) Primality Test)",
                    "description": "Tests if an integer is prime by trial division up to sqrt(n) with 6k +/- 1 optimization.",
                    "code": """```python
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

test_nums = [2, 3, 4, 17, 19, 20, 97, 100]
for x in test_nums:
    print(f"{x} is prime: {is_prime(x)}")
```"""
                }
            elif target_lang in ["cpp", "c"]:
                return {
                    "id": "dyn_cpp_prime",
                    "languages": [target_lang],
                    "title": f"Prime Number Verification in {target_lang.upper()}",
                    "description": "Tests primality in O(sqrt(n)) time.",
                    "code": f"""```{target_lang}
#include <iostream>

bool is_prime(long long n) {{
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (long long i = 5; i * i <= n; i += 6) {{
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }}
    return true;
}}

int main() {{
    std::cout << "97 is prime: " << (is_prime(97) ? "true" : "false") << std::endl;
    return 0;
}}
```"""
                }

        if any(w in clean for w in ["greatest common divisor", "gcd", "euclidean algorithm"]):
            if target_lang == "python":
                return {
                    "id": "dyn_py_gcd",
                    "languages": ["python"],
                    "title": "Greatest Common Divisor (Euclidean Algorithm)",
                    "description": "Computes the GCD and LCM of two integers in logarithmic O(log(min(a, b))) time.",
                    "code": """```python
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)

print("GCD(48, 18):", gcd(48, 18))
print("LCM(48, 18):", lcm(48, 18))
```"""
                }
            elif target_lang in ["cpp", "c"]:
                return {
                    "id": "dyn_cpp_gcd",
                    "languages": [target_lang],
                    "title": f"Greatest Common Divisor in {target_lang.upper()}",
                    "description": "Computes GCD using the Euclidean algorithm.",
                    "code": f"""```{target_lang}
#include <iostream>

long long gcd(long long a, long long b) {{
    while (b != 0) {{
        long long t = b;
        b = a % b;
        a = t;
    }}
    return a;
}}

int main() {{
    std::cout << "GCD(48, 18) = " << gcd(48, 18) << std::endl;
    return 0;
}}
```"""
                }

        if any(w in clean for w in ["reverse string", "reverse a string"]):
            if target_lang == "python":
                return {
                    "id": "dyn_py_rev_str",
                    "languages": ["python"],
                    "title": "String Reversal (Slice & Two-Pointer In-Place)",
                    "description": "Demonstrates string reversal using extended slicing and character list two-pointer swap.",
                    "code": """```python
def reverse_string_slice(s: str) -> str:
    return s[::-1]

def reverse_char_list(chars: list) -> None:
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1

word = "OfflineAI"
print("Reversed slice:", reverse_string_slice(word))
arr = list(word)
reverse_char_list(arr)
print("Reversed in-place:", "".join(arr))
```"""
                }
            elif target_lang in ["javascript", "typescript"]:
                return {
                    "id": "dyn_js_rev_str",
                    "languages": [target_lang],
                    "title": "String Reversal in JavaScript",
                    "description": "Reverses string using split-reverse-join.",
                    "code": """```javascript
function reverseString(str) {
  return str.split("").reverse().join("");
}

console.log(reverseString("Hello World"));
```"""
                }
            elif target_lang in ["cpp", "c"]:
                return {
                    "id": "dyn_cpp_rev_str",
                    "languages": [target_lang],
                    "title": f"String Reversal in {target_lang.upper()}",
                    "description": "Reverses a string in-place using two pointers.",
                    "code": f"""```{target_lang}
#include <iostream>
#include <string>
#include <algorithm>

void reverse_inplace(std::string& s) {{
    int l = 0, r = s.length() - 1;
    while (l < r) {{
        std::swap(s[l++], s[r--]);
    }}
}}

int main() {{
    std::string text = "Offline AI";
    reverse_inplace(text);
    std::cout << text << std::endl;
    return 0;
}}
```"""
                }

        if "bubble sort" in clean:
            if target_lang == "python":
                return {
                    "id": "dyn_py_bubble_sort",
                    "languages": ["python"],
                    "title": "Bubble Sort (Optimized with Early Stopping O(n^2))",
                    "description": "Sorts an array by repeatedly swapping adjacent elements with a swapped flag for O(n) best-case time.",
                    "code": """```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

data = [64, 34, 25, 12, 22, 11, 90]
print("Sorted:", bubble_sort(data))
```"""
                }
            elif target_lang in ["cpp", "c"]:
                return {
                    "id": "dyn_cpp_bubble_sort",
                    "languages": [target_lang],
                    "title": f"Bubble Sort in {target_lang.upper()}",
                    "description": "Optimized bubble sort algorithm with early termination.",
                    "code": f"""```{target_lang}
#include <iostream>
#include <vector>
#include <utility>

void bubble_sort(std::vector<int>& arr) {{
    size_t n = arr.size();
    for (size_t i = 0; i < n; ++i) {{
        bool swapped = false;
        for (size_t j = 0; j < n - i - 1; ++j) {{
            if (arr[j] > arr[j + 1]) {{
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }}
        }}
        if (!swapped) break;
    }}
}}

int main() {{
    std::vector<int> data = {{64, 34, 25, 12, 22, 11, 90}};
    bubble_sort(data);
    for (int x : data) std::cout << x << " ";
    std::cout << std::endl;
    return 0;
}}
```"""
                }

        return None

    def format_solution(self, recipe: Dict[str, Any]) -> str:
        lines = [
            f"### 💻 {recipe.get('title')}",
            f"\n**Language / Ecosystem:** `{', '.join(recipe.get('languages', []))}`",
            f"**Overview:** {recipe.get('description')}\n",
            recipe.get("code", "").strip()
        ]
        return "\n".join(lines)
