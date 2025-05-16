const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');

router.post('/feedback', (req, res) => {
  const { feedbackText } = req.body;
  console.log("Received feedbackText from client:", feedbackText);

  // Build absolute path to feedback_model.py
  const scriptPath = path.join(__dirname, '..', 'models', 'ml', 'feedback_model.py');

  const python = spawn('python', [scriptPath]);

  let result = '';

  python.stdout.on('data', (data) => {
    result += data.toString();
  });

  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on('close', () => {
    res.json({ prediction: result.trim() });
  });

  python.stdin.write(feedbackText + '\n');
  python.stdin.end();
});

module.exports = router;

