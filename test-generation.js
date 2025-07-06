import { compileFromFile } from "json-schema-to-typescript";

async function test() {
  console.log("Testing schema generation...");
  
  try {
    console.log("Generating beat-data...");
    const beatTs = await compileFromFile("schemas/beat-data.json");
    console.log("Beat data generated successfully, length:", beatTs.length);
    
    console.log("Generating sequence-data...");
    const sequenceTs = await compileFromFile("schemas/sequence-data.json");
    console.log("Sequence data generated successfully, length:", sequenceTs.length);
    
  } catch (error) {
    console.error("Error:", error);
  }
}

test();
