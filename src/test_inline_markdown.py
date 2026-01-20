import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_delimiter, 
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes
)

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("`code1` and some text `code2` end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("code1", TextType.CODE),
            TextNode(" and some text ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_nodes_delimiter_unclosed(self):
        node = TextNode("This is an `unclosed code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
            
    def test_split_nodes_delimiter_no_formatting(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [TextNode("Just some plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )
        
    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com) inside."
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)
        
    def test_extract_multiple_links_and_images(self):
        text = "Here is an ![image1](http://image1.png) and a [link1](http://link1.com). Also, ![image2](http://image2.png) with [link2](http://link2.com)."
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual(
            [("image1", "http://image1.png"), ("image2", "http://image2.png")],
            image_matches,
        )
        self.assertListEqual(
            [("link1", "http://link1.com"), ("link2", "http://link2.com")],
            link_matches,
        )
        
    def test_no_matches(self):
        text = "This text has no markdown links or images."
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([], image_matches)
        self.assertListEqual([], link_matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_no_images(self):
        node = TextNode("This is text without images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_images_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)
        
    def test_split_images_only_image(self):
        node = TextNode("![only image](http://onlyimage.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("only image", TextType.IMAGE, "http://onlyimage.png")],
            new_nodes,
        )
        
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) inside.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" inside.", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected_nodes, nodes)
        
    def test_text_to_text_nodes_no_formatting(self):
        text = "Just some plain text without any formatting."
        nodes = text_to_text_nodes(text)
        expected_nodes = [TextNode(text, TextType.TEXT)]
        self.assertListEqual(expected_nodes, nodes)
        
    def test_text_to_text_nodes_only_formatting(self):
        text = "**bold** _italic_ `code` ![alt](url) [link](url)"
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected_nodes, nodes)
        
    def test_text_to_text_nodes_nested_formatting(self):
        text = "**bold and _italic_**"
        nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("bold and _italic_", TextType.BOLD)
        ]
        self.assertListEqual(expected_nodes, nodes)
        
    def test_text_to_text_nodes_unclosed_delimiter(self):
        text = "This is **bold text with no end"
        with self.assertRaises(ValueError):
            text_to_text_nodes(text)
            
if __name__ == "__main__":
    unittest.main()