const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const required = [
  "index.html",
  "styles.css",
  "app.js",
  "assets/lucerna-mark.svg",
  "api/analyze.py",
  "backend/config.py",
  "backend/llm.py",
  "backend/tree_engine.py",
  "backend/rules.py",
  "backend/report.py",
  "content/questions/ca/tree.json",
  "content/ontology/indicators.json",
  "content/ontology/recommendations.json",
  "content/ontology/sources.json",
  "content/resources/barcelona.json",
  "content/training_cases/cases.json",
  "docs/SYSTEM.md",
  "README.md"
];

for (const file of required) {
  const target = path.join(root, file);
  if (!fs.existsSync(target)) {
    throw new Error(`Falta ${file}`);
  }
}

for (const jsonFile of required.filter((file) => file.endsWith(".json"))) {
  JSON.parse(fs.readFileSync(path.join(root, jsonFile), "utf8"));
}

const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const js = fs.readFileSync(path.join(root, "app.js"), "utf8");

for (const text of [
  "LUCERNA 65",
  "profileSelect",
  "localeToggle",
  "answerPanel",
  "factExtractor",
  "reportPanel",
  "/api/session/start",
  "/api/session/answer",
  "/api/text/facts",
  "/api/report"
]) {
  if (!html.includes(text) && !js.includes(text)) {
    throw new Error(`No s'ha trobat el text obligatori: ${text}`);
  }
}

console.log("Validacio correcta.");

