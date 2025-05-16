const express = require('express');
const router = express.Router();
const Medicine = require('../models/medicineModel');

// @route   GET /api/medicines
// @desc    Get all medicines
router.get('/', async (req, res) => {
  try {
    const medicines = await Medicine.find();
    res.json(medicines);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// @route   POST /api/medicines
// @desc    Add a new medicine
router.post('/', async (req, res) => {
  const { name, uses, sustainableAlternative, environmentalImpactScore } = req.body;

  const newMedicine = new Medicine({
    name,
    uses,
    sustainableAlternative,
    environmentalImpactScore,
  });

  try {
    const savedMedicine = await newMedicine.save();
    res.status(201).json(savedMedicine);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

module.exports = router;
