const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(express.json());

// File path for storing expenses
const expensesFile = path.join(__dirname, 'expenses.json');

// Helper function to read expenses
const readExpenses = () => {
  try {
    if (fs.existsSync(expensesFile)) {
      const data = fs.readFileSync(expensesFile, 'utf-8');
      return JSON.parse(data);
    }
    return [];
  } catch (error) {
    console.error('Error reading expenses:', error);
    return [];
  }
};

// Helper function to write expenses
const writeExpenses = (expenses) => {
  try {
    fs.writeFileSync(expensesFile, JSON.stringify(expenses, null, 2));
  } catch (error) {
    console.error('Error writing expenses:', error);
  }
};

// Routes

// GET all expenses
app.get('/api/expenses', (req, res) => {
  const expenses = readExpenses();
  res.json(expenses);
});

// POST a new expense
app.post('/api/expenses', (req, res) => {
  const { description, amount, category, date } = req.body;

  if (!description || !amount || !category) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const expenses = readExpenses();
  const newExpense = {
    id: Date.now(),
    description,
    amount: parseFloat(amount),
    category,
    date: date || new Date().toLocaleDateString(),
  };

  expenses.push(newExpense);
  writeExpenses(expenses);

  res.status(201).json(newExpense);
});

// DELETE an expense
app.delete('/api/expenses/:id', (req, res) => {
  const { id } = req.params;
  let expenses = readExpenses();

  const initialLength = expenses.length;
  expenses = expenses.filter(exp => exp.id !== parseInt(id));

  if (expenses.length === initialLength) {
    return res.status(404).json({ error: 'Expense not found' });
  }

  writeExpenses(expenses);
  res.json({ message: 'Expense deleted successfully' });
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'Server is running' });
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Backend server is running on http://localhost:${PORT}`);
  console.log(`📝 Expenses data stored in: ${expensesFile}`);
});
