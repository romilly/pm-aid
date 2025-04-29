// layout.js
import fs from 'fs';
import { layoutProcess } from 'bpmn-auto-layout';

// Get command line arguments
const inputFile = process.argv[2];
const outputFile = process.argv[3];

if (!inputFile || !outputFile) {
  console.error('Usage: node layout.js <input-bpmn-file> <output-bpmn-file>');
  process.exit(1);
}

// Define an async function to use await
async function processFile() {
  try {
    // Read the input BPMN XML
    const diagramXML = fs.readFileSync(inputFile, 'utf8');
    
    // Apply layout using the example code syntax
    const diagramWithLayoutXML = await layoutProcess(diagramXML);
    
    // Write the result to the output file
    fs.writeFileSync(outputFile, diagramWithLayoutXML, 'utf8');
    console.log(`Auto layout applied. Result saved to ${outputFile}`);
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

// Execute the async function
processFile();