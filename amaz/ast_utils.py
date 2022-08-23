import ast
import codecs


class AsTra(ast.NodeTransformer):
    def visit_Constant(self, node):
        if isinstance(node.value, str):
            node.value = codecs.encode(node.value, "rot_13")
        return node

    def visit_Str(self, node):
        node.s = codecs.encode(node.s, "rot_13")
        return node

    def visit_Name(self, node):
        node.id = codecs.encode(node.id, "rot_13")
        return node
