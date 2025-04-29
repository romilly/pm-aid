# PM-Aid: Process Modeling Aid

A Python tool for creating, parsing, and exporting Business Process Model and Notation (BPMN) diagrams using a simplified YAML format.

## Overview

PM-Aid allows you to define business processes in a simple YAML format and convert them to standard BPMN 2.0 XML files that can be used with other BPMN tools and viewers. The tool provides:

- A simplified YAML syntax for defining processes
- Automatic conversion to standard BPMN 2.0 XML
- Auto-layout capabilities for visual representation

## Road Map

The current version is minimal; it was written as a proof of concept and has no tests.


Next steps:
* add tests!
* automate layout
* add pool, lanes to YAML schema and code
* add sub-processes, documents and data sources.
* add code to get AI to generate the YAML from English text.

In the long term, I want to build a DSL that will include process definition, Planguage specifications for projects and products, EVO processes, process libraries and support for Wardley mapping.

I also want to build a web app that will allow users to create and manage their processes.


## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pm-aid.git
cd pm-aid

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

1. Create a YAML file defining your process (see [Examples](#examples))
2. Convert it to BPMN using the convert module:

```python
from pm_aid.convert import convert_yaml_to_bpmn

# Convert YAML to BPMN
bpmn_file = convert_yaml_to_bpmn("path/to/your/process.yaml")
print(f"BPMN file created at: {bpmn_file}")
```

### Command Line

You can also use the module directly from the command line:

```bash
python -m pm_aid.convert path/to/your/process.yaml
```

## YAML Format

Define your process in YAML with the following structure:

```yaml
process:
  id: unique_process_id
  name: Process Name
  description: Process Description
  steps:
    - type: start
      id: start_id
      name: Start Event Name
      next: next_step_id

    - type: task
      id: task_id
      name: Task Name
      description: Task Description
      next: next_step_id

    # More steps...
```

### Supported Element Types

- `start`: Start event
- `end`: End event
- `task`: Activity or task
- `decision`: Exclusive gateway (decision point)
- `merge`: Exclusive gateway (merge point)
- `parallel_split`: Parallel gateway (fork)
- `parallel_join`: Parallel gateway (join)

### Flow Control

For simple flows, use the `next` property with the ID of the next element:

```yaml
- type: task
  id: task1
  next: task2
```

For conditional flows (after decisions), use a dictionary:

```yaml
- type: decision
  id: check_condition
  next:
    yes: approved_task
    no: rejected_task
```

## Examples

See the `examples` directory for complete examples:

- `breadboard-project.yaml`: A process for assembling an electronics breadboard project

![Breadboard Process Example](docs/img/breadboard-eg.svg)

## Project Structure

- `pm_aid/`: Core package
  - `model.py`: BPMN data model classes
  - `parser.py`: YAML parser
  - `export.py`: BPMN XML exporter
  - `convert.py`: Conversion utilities
- `examples/`: Example process definitions
- `docs/`: Documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
