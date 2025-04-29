from typing import List, Optional, Dict

class BPMNElement:
    def __init__(self, id: str, name: Optional[str] = None):
        self.id = id
        self.name = name

class Lane(BPMNElement):
    def __init__(self, id: str, name: Optional[str] = None):
        super().__init__(id, name)
        self.elements: List[BPMNElement] = []

    def add_element(self, element: BPMNElement):
        self.elements.append(element)

class Pool(BPMNElement):
    def __init__(self, id: str, name: Optional[str] = None):
        super().__init__(id, name)
        self.lanes: List[Lane] = []
        self.elements: List[BPMNElement] = []  # For elements not in lanes

    def add_lane(self, lane: Lane):
        self.lanes.append(lane)

    def add_element(self, element: BPMNElement):
        self.elements.append(element)

class Event(BPMNElement):
    def __init__(self, id: str, name: Optional[str] = None, event_type: str = 'start'):
        super().__init__(id, name)
        self.event_type = event_type  # 'start', 'end', 'intermediate'

class Task(BPMNElement):
    def __init__(self, id: str, name: Optional[str] = None):
        super().__init__(id, name)

class Gateway(BPMNElement):
    def __init__(self, id: str, name: Optional[str] = None, gateway_type: str = 'exclusive'):
        super().__init__(id, name)
        self.gateway_type = gateway_type  # 'exclusive', 'parallel', 'inclusive'

class SequenceFlow:
    def __init__(self, id: str, source: BPMNElement, target: BPMNElement, condition: Optional[str] = None):
        self.id = id
        self.source = source
        self.target = target
        self.condition = condition

class Process:
    def __init__(self, id: str, name: Optional[str] = None):
        self.id = id
        self.name = name
        self.pools: List[Pool] = []
        self.elements: List[BPMNElement] = []  # For elements not in pools
        self.flows: List[SequenceFlow] = []

    def add_pool(self, pool: Pool):
        self.pools.append(pool)

    def add_element(self, element: BPMNElement):
        self.elements.append(element)

    def add_flow(self, flow: SequenceFlow):
        self.flows.append(flow)

    def find_element(self, id: str) -> Optional[BPMNElement]:
        # Search in root elements
        for element in self.elements:
            if element.id == id:
                return element
        
        # Search in pools and lanes
        for pool in self.pools:
            for element in pool.elements:
                if element.id == id:
                    return element
            for lane in pool.lanes:
                for element in lane.elements:
                    if element.id == id:
                        return element
        return None
