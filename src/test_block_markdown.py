import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_empty_lines(self):
        md = """
        
        
This is a paragraph


"""      
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
            ],
        )
        
    def test_markdown_to_blocks_only_empty(self):
        md = """
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        
    def test_block_to_block_type(self):
        self.assertEqual(
            block_to_block_type("# Heading 1"),
            BlockType.HEADING,
        )
        self.assertEqual(
            block_to_block_type("```python\nprint('Hello')\n```"),
            BlockType.CODE,
        )
        self.assertEqual(
            block_to_block_type("> This is a quote"),
            BlockType.QUOTE,
        )
        self.assertEqual(
            block_to_block_type("- Unordered list item"),
            BlockType.UNORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("1. Ordered list item"),
            BlockType.ORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("This is a normal paragraph."),
            BlockType.PARAGRAPH,
        )
        
    def test_block_to_block_type_edge_cases(self):
        self.assertEqual(
            block_to_block_type("##Heading without space"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("```Not a code block"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("Just a > symbol"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("2.Ordered list without space"),
            BlockType.PARAGRAPH,
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )