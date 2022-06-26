# Wiki
 
Access to Wikipedia via the command line


```
wiki -h                                             
usage: wiki [-h] {search,open} ...

Access to Wikipedia via the command line

positional arguments:
  {search,open}
    search       search {title} {options}.
    open         open {title} {options}.
```

```
wiki open "Architecture" --whole                              
╭──────────────────────────────────────────────────────────────────────────────╮
│ Architecture                                                                 │
│ Link: https://en.wikipedia.org/wiki/Architecture                             │
│                                                                              │
│ Architecture (Latin architectura, from the Greek ἀρχιτέκτων arkhitekton      │
│ "architect", from ἀρχι- "chief" and τέκτων "creator") is both the process    │
...
```