"""Export BPMN models to BPMN 2.0 XML format."""
from typing import Dict, Optional
import xml.etree.ElementTree as ET
from xml.dom import minidom
from .model import Process, Event, Task, Gateway, SequenceFlow

BPMN20_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
BPMNDI_NS = "http://www.omg.org/spec/BPMN/20100524/DI"
DC_NS = "http://www.omg.org/spec/DD/20100524/DC"
DI_NS = "http://www.omg.org/spec/DD/20100524/DI"

class BPMNExporter:
    def __init__(self):
        self.ns = {
            "bpmn": BPMN20_NS,
            "bpmndi": BPMNDI_NS,
            "dc": DC_NS,
            "di": DI_NS
        }
        
    def export_process(self, process: Process, output_path: str, auto_layout: bool = True) -> None:
        """Export a Process to BPMN 2.0 XML format.
        
        Args:
            process: The Process to export
            output_path: Path where to save the .bpmn file
            auto_layout: Whether to automatically generate layout information
        """
        # Create the root element with namespaces
        definitions = ET.Element(f"{{{BPMN20_NS}}}definitions")
        for prefix, uri in self.ns.items():
            definitions.set(f"xmlns:{prefix}", uri)
        
        # Create the process element
        process_elem = ET.SubElement(definitions, f"{{{BPMN20_NS}}}process")
        process_elem.set("id", process.id)
        if process.name:
            process_elem.set("name", process.name)
        
        # Add all flow elements
        self._add_flow_elements(process_elem, process)
        
        # Add diagram information if auto_layout is enabled
        if auto_layout:
            self._add_diagram(definitions, process)
        
        # Write the XML file
        tree = ET.ElementTree(definitions)
        xml_str = ET.tostring(definitions, encoding='unicode')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
    
    def _add_flow_elements(self, process_elem: ET.Element, process: Process) -> None:
        """Add all flow elements (events, tasks, gateways, sequence flows) to the process."""
        for element in process.elements:
            if isinstance(element, Event):
                event_elem = ET.SubElement(
                    process_elem,
                    f"{{{BPMN20_NS}}}{element.event_type}Event"
                )
                event_elem.set("id", element.id)
                if element.name:
                    event_elem.set("name", element.name)
                    
            elif isinstance(element, Task):
                task_elem = ET.SubElement(process_elem, f"{{{BPMN20_NS}}}task")
                task_elem.set("id", element.id)
                if element.name:
                    task_elem.set("name", element.name)
                    
            elif isinstance(element, Gateway):
                gateway_type = (
                    "parallel" if element.gateway_type == "parallel" else "exclusive"
                )
                gateway_elem = ET.SubElement(
                    process_elem,
                    f"{{{BPMN20_NS}}}{gateway_type}Gateway"
                )
                gateway_elem.set("id", element.id)
                if element.name:
                    gateway_elem.set("name", element.name)
        
        # Add sequence flows after all nodes are created
        for flow in process.flows:
            flow_elem = ET.SubElement(process_elem, f"{{{BPMN20_NS}}}sequenceFlow")
            flow_elem.set("id", flow.id)
            flow_elem.set("sourceRef", flow.source.id)
            flow_elem.set("targetRef", flow.target.id)
            
            if flow.condition:
                condition_elem = ET.SubElement(
                    flow_elem,
                    f"{{{BPMN20_NS}}}conditionExpression"
                )
                condition_elem.text = flow.condition
    
    def _add_diagram(self, definitions: ET.Element, process: Process) -> None:
        """Add BPMN DI (Diagram Interchange) information for visualization."""
        diagram = ET.SubElement(definitions, f"{{{BPMNDI_NS}}}BPMNDiagram")
        diagram.set("id", f"BPMNDiagram_{process.id}")
        
        plane = ET.SubElement(diagram, f"{{{BPMNDI_NS}}}BPMNPlane")
        plane.set("id", f"BPMNPlane_{process.id}")
        plane.set("bpmnElement", process.id)
        
        # Simple auto-layout: arrange elements in a grid
        grid_size = 150
        elements_per_row = 3
        current_x = 100
        current_y = 100
        element_positions: Dict[str, tuple] = {}
        
        # Position nodes
        for i, element in enumerate(process.elements):
            row = i // elements_per_row
            col = i % elements_per_row
            x = current_x + (col * grid_size)
            y = current_y + (row * grid_size)
            element_positions[element.id] = (x, y)
            
            shape = ET.SubElement(plane, f"{{{BPMNDI_NS}}}BPMNShape")
            shape.set("id", f"BPMNShape_{element.id}")
            shape.set("bpmnElement", element.id)
            
            bounds = ET.SubElement(shape, f"{{{DC_NS}}}Bounds")
            bounds.set("x", str(x))
            bounds.set("y", str(y))
            bounds.set("width", "100")
            bounds.set("height", "80")
        
        # Add sequence flow visualization
        for flow in process.flows:
            edge = ET.SubElement(plane, f"{{{BPMNDI_NS}}}BPMNEdge")
            edge.set("id", f"BPMNEdge_{flow.id}")
            edge.set("bpmnElement", flow.id)
            
            # Create a simple straight line between elements
            source_pos = element_positions[flow.source.id]
            target_pos = element_positions[flow.target.id]
            
            # Source point
            waypoint = ET.SubElement(edge, f"{{{DI_NS}}}waypoint")
            waypoint.set("x", str(source_pos[0] + 50))  # Center of shape
            waypoint.set("y", str(source_pos[1] + 40))
            
            # Target point
            waypoint = ET.SubElement(edge, f"{{{DI_NS}}}waypoint")
            waypoint.set("x", str(target_pos[0] + 50))
            waypoint.set("y", str(target_pos[1] + 40))