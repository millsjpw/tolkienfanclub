import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", {"class": "container"})
        node2 = HTMLNode("div", {"class": "container"})
        self.assertEqual(node, node2)
        
    def test_neq_different_tag(self):
        node = HTMLNode("div", {"class": "container"})
        node2 = HTMLNode("span", {"class": "container"})
        self.assertNotEqual(node, node2)
        
    def test_neq_different_attributes(self):
        node = HTMLNode("div", {"class": "container"})
        node2 = HTMLNode("div", {"id": "main"})
        self.assertNotEqual(node, node2)
    
    def test_neq_different_children(self):
        node = HTMLNode("div", {}, [HTMLNode("p")])
        node2 = HTMLNode("div", {}, [HTMLNode("span")])
        self.assertNotEqual(node, node2)
        
    def test_neq_children_vs_no_children(self):
        node = HTMLNode("div", {}, [HTMLNode("p")])
        node2 = HTMLNode("div", {})
        self.assertNotEqual(node, node2)
        
    def test_props_to_html(self):
        node = HTMLNode("a", {}, props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')
        
    def test_props_to_html_no_props(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), '')
        
class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        leaf = LeafNode("p", "Hello, World!", props={"class": "text"})
        self.assertEqual(leaf.to_html(), '<p class="text">Hello, World!</p>')
        
    def test_to_html_with_value_only(self):
        leaf = LeafNode(None, "Just some text")
        self.assertEqual(leaf.to_html(), 'Just some text')
        
    def test_to_html_no_value_raises(self):
        leaf = LeafNode("p", None)
        with self.assertRaises(ValueError):
            leaf.to_html()
            
    def test_anchor_with_href(self):
        leaf = LeafNode("a", "Click here", props={"href": "https://example.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://example.com">Click here</a>')
        
    def test_image_with_src(self):
        leaf = LeafNode("img", None, props={"src": "image.png", "alt": "An image"})
        with self.assertRaises(ValueError):
            leaf.to_html()
            
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        parent = ParentNode("div", [child1, child2], props={"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><p>Paragraph 1</p><p>Paragraph 2</p></div>')
        
    def test_to_html_no_tag_raises(self):
        child = LeafNode("p", "Paragraph")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()
            
    def test_to_html_no_children_raises(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()
    def test_has_values(self):
        child = LeafNode("span", "Child")
        parent = ParentNode("div", [child], props={"id": "main"})
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, {"id": "main"})
        
    def test_neq_different_props(self):
        child = LeafNode("p", "Paragraph")
        parent1 = ParentNode("div", [child], props={"class": "container"})
        parent2 = ParentNode("div", [child], props={"id": "main"})
        self.assertNotEqual(parent1, parent2)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
        
if __name__ == "__main__":
    unittest.main()