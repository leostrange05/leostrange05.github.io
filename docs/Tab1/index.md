---
title: "Branch Example"
---
<!-- This is the title shown in the browser tab -->

# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

```cpp
#include <iostream>
int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

```python
def greet():
    print("Hello, World!")
greet()
```

```verilog
module hello_world;
  initial begin
    $display("Hello, World!");
    $finish;
  end
endmodule
```

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## 中文测试

正文中文，正文中文？正文中文。“正文中文”；《正文中文》——正文中文‘正文中文’。、

**加粗**



    代码块中文

# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## 中文测试

正文中文，正文中文？正文中文。“正文中文”；《正文中文》——正文中文‘正文中文’。、

**加粗**



    代码块中文

# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## 中文测试

正文中文，正文中文？正文中文。“正文中文”；《正文中文》——正文中文‘正文中文’。、

**加粗**



    代码块中文


!!! note

    This is a warning message.

!!! warning "This is a warning"

    This is a warning message.

??? info "This is an info"

    This is an info message.

!!! success

    This is a success message.

!!! question "This is a question"

    This is a question message.

???+ failure "This is a failure"

    This is a failure message.

!!! bug

    This is a bug message.

!!! example "This is an example"

    This is an example message.