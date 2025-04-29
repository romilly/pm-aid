"""Parser for YAML-based BPMN process definitions."""
from pathlib import Path
from typing import Dict, Optional, Union
import yaml

from .model import BPMNElement, Event, Task, Gateway, Process, SequenceFlow

class BPMNParser:
    def __init__(self):
        self.elements: Dict[str, BPMNElement] = {}
        
    def parse_file(self, yaml_path: Union[str, Path]) -> Process:
        """Parse a YAML file into a BPMN Process."""
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        return self.parse_dict(data)
    
    def parse_dict(self, data: dict) -> Process:
        """Parse a dictionary into a BPMN Process."""
        process_data = data['process']
        process = Process(
            id=process_data['id'],
            name=process_data.get('name')
        )
        
        # First pass: create all elements
        for step in process_data['steps']:
            element = self._create_element(step)
            process.add_element(element)
            self.elements[element.id] = element
            
        # Second pass: create sequence flows
        for step in process_data['steps']:
            if 'next' in step:
                self._create_flows(process, step)
                
        return process
    
    def _create_element(self, step: dict) -> BPMNElement:
        """Create a BPMN element based on its type."""
        element_type = step['type']
        element_id = step['id']
        element_name = step.get('name')
        
        if element_type in ('start', 'end'):
            return Event(
                id=element_id,
                name=element_name,
                event_type=element_type
            )
        elif element_type == 'task':
            return Task(
                id=element_id,
                name=element_name
            )
        elif element_type in ('decision', 'merge', 'parallel_split', 'parallel_join'):
            gateway_type = 'exclusive'
            if element_type in ('parallel_split', 'parallel_join'):
                gateway_type = 'parallel'
            return Gateway(
                id=element_id,
                name=element_name,
                gateway_type=gateway_type
            )
        else:
            raise ValueError(f"Unknown element type: {element_type}")
    
    def _create_flows(self, process: Process, step: dict) -> None:
        """Create sequence flows from an element to its next elements."""
        source_id = step['id']
        source = self.elements[source_id]
        next_info = step['next']
        
        if isinstance(next_info, str):
            # Simple flow
            target = self.elements[next_info]
            flow = SequenceFlow(
                id=f"flow_{source_id}_{next_info}",
                source=source,
                target=target
            )
            process.add_flow(flow)
        else:
            # Conditional flows
            for condition, target_id in next_info.items():
                target = self.elements[target_id]
                flow = SequenceFlow(
                    id=f"flow_{source_id}_{target_id}",
                    source=source,
                    target=target,
                    condition=condition
                )
                process.add_flow(flow)