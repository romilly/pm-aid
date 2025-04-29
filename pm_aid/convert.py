from pathlib import Path
from typing import Union
from pm_aid.parser import BPMNParser
from pm_aid.export import BPMNExporter

def convert_yaml_to_bpmn(file_path: Union[str, Path], auto_layout: bool = True) -> Path:
    """Convert a YAML process definition to BPMN format.
    
    Args:
        file_path: Path to the YAML file
        auto_layout: Whether to automatically generate layout information
        
    Returns:
        Path to the generated BPMN file
        
    Example:
        >>> bpmn_file = convert_yaml_to_bpmn("process.yaml")
        >>> print(f"BPMN file created at: {bpmn_file}")
    """
    # Convert to Path object for easier manipulation
    yaml_path = Path(file_path)
    
    # Validate input file exists and is YAML
    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML file not found: {yaml_path}")
    if yaml_path.suffix.lower() not in ['.yaml', '.yml']:
        raise ValueError(f"Input file must be a YAML file, got: {yaml_path}")
    
    # Create output path with .bpmn extension
    bpmn_path = yaml_path.with_suffix('.bpmn')
    
    # Initialize parser and exporter
    parser = BPMNParser()
    exporter = BPMNExporter()
    
    try:
        # Parse YAML to process
        process = parser.parse_file(yaml_path)
        
        # Export process to BPMN
        exporter.export_process(
            process=process,
            output_path=str(bpmn_path),
            auto_layout=auto_layout
        )
        
        return bpmn_path
        
    except Exception as e:
        raise RuntimeError(f"Error converting {yaml_path} to BPMN: {str(e)}") from e

if __name__ == "__main__":
    convert_yaml_to_bpmn('../examples/breadboard-project.yaml')