# codewars code gymnastics
Notes from working through the codewars katas.

### Four Pass Transport

Blind4Basics published an interesting solution with just 70 source lines of code (sloc) vs. the 470 sloc I needed for my solution.

```python
def convert(pos):
    row = pos // 10
   	col = pos % 10
   	return row, col
```

