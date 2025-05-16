const mongoose = require('mongoose');

// Define the schema for the medicine
const medicineSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,  // Medicine name is required
  },
  uses: {
    type: String,   // The uses of the medicine
  },
  sustainableAlternative: {
    type: String,   // Sustainable alternatives (if any)
  },
  environmentalImpactScore: {
    type: Number,   // A score between 1 and 10 to rate the impact
    min: 1,         // Minimum score is 1
    max: 10,        // Maximum score is 10
  },
}, {
  timestamps: true,  // Automatically adds createdAt and updatedAt fields
});

// Create the model
const Medicine = mongoose.model('Medicine', medicineSchema);

// Export the model to use in other files
module.exports = Medicine;
