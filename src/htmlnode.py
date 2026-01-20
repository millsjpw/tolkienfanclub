class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html method")
    
    def props_to_html(self):
        props_str = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        return f' {props_str}' if props_str else ''
    
    def __eq__(self, other):
        return (self.tag == other.tag and 
                self.value == other.value and 
                self.children == other.children and 
                self.props == other.props)
    
    def __repr__(self):
        print(f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})")
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=[], props=props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML")
        children_html = ''.join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"