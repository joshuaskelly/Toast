class QuadTree(object):
    def __init__(self, items, region):
        
        self.quadrant = region
        
        self.width = region[2]
        self.height = region[3]
        
        self.left = region[0]
        self.top = region[1]
        self.right = self.left + self.width
        self.bottom = self.top + self.height
        
        self.half_width = self.width / 2
        self.half_height = self.height / 2
        
        # Create the sub-blocks
        self.northwest_tree = None
        self.northeast_tree = None
        self.southwest_tree = None
        self.southeast_tree = None
        
        self.bucket = []
        
        for item in items:
            self.insert(item)
            
    def create_subtrees(self):
        if self.width < 8:
            return False
        
        if self.northwest_tree:
            return True
        
        self.northwest_tree = QuadTree([], (self.left, self.top, self.half_width, self.half_height))
        self.northeast_tree = QuadTree([], (self.left + self.half_width, self.top, self.half_width, self.half_height))
        self.southwest_tree = QuadTree([], (self.left, self.top + self.half_height, self.half_width, self.half_height))
        self.southeast_tree = QuadTree([], (self.left + self.half_height, self.top + self.half_height, self.half_width, self.half_height))
        
        return True
        
    def insert(self, item):
        in_nw = False
        in_ne = False
        in_sw = False
        in_se = False
        
        l, t, w, h = self.quadrant
        cx, cy = l + (w/2), t + (h/2)
        
        il = item[0]
        it = item[1]
        ir = il + item[2]
        ib = it + item[3]
        
        in_nw = il < cx and it < cy
        in_sw = il < cx and ib > cy
        in_ne = ir > cx and it < cy
        in_se = ir > cx and ib > cy

        # If the rect overlaps boundaries or we have hit our minimum block size
        if len([x for x in [in_nw, in_ne, in_sw, in_se] if x]) > 1 or not self.create_subtrees():
            self.bucket.append(item)
        elif in_nw:
            self.northwest_tree.insert(item)
        elif in_ne:
            self.northeast_tree.insert(item)
        elif in_sw:
            self.southwest_tree.insert(item)
        elif in_se:
            self.southeast_tree.insert(item)
            
    def hit(self, rect):
        def contains(item):
            return rect[0] < item[0] + item[2] and \
                   rect[0] + rect[2] > item[0] and \
                   rect[1] < item[1] + item[3] and \
                   rect[1] + rect[3] > item[1]

        # Check items in bucket
        result = [item for item in self.bucket if contains(item)]
           
        # Recurse     
        if self.northwest_tree:
            if rect[0] < self.left + self.half_width and \
               rect[1] < self.top + self.half_height:
                result += self.northwest_tree.hit(rect)
                
            if rect[0] < self.left + self.half_width and \
               rect[1] + rect[3] > self.top + self.half_height:
                result += self.southwest_tree.hit(rect)
                
            if rect[0] + rect[2] > self.left + self.half_width and \
               rect[1] < self.top + self.half_height:
                result += self.northeast_tree.hit(rect)
                
            if rect[0] + rect[2] > self.left + self.half_width and \
               rect[1] + rect[3] > self.top + self.half_height:
                result += self.southeast_tree.hit(rect)
        
        return result
            