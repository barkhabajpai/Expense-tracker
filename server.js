const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const { PythonShell } = require('python-shell');

const app = express();
const PORT = 5000;
const ML_SERVER_URL = 'http://localhost:5001';

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

// GET a specific expense by ID
app.get('/api/expenses/:id', (req, res) => {
  const { id } = req.params;
  const expenses = readExpenses();
  const expense = expenses.find(exp => exp.id === parseInt(id));

  if (!expense) {
    return res.status(404).json({ error: 'Expense not found' });
  }

  res.json(expense);
});

// UPDATE an expense
app.put('/api/expenses/:id', (req, res) => {
  const { id } = req.params;
  const { description, amount, category, date } = req.body;
  let expenses = readExpenses();

  const expenseIndex = expenses.findIndex(exp => exp.id === parseInt(id));

  if (expenseIndex === -1) {
    return res.status(404).json({ error: 'Expense not found' });
  }

  expenses[expenseIndex] = {
    ...expenses[expenseIndex],
    description: description || expenses[expenseIndex].description,
    amount: amount !== undefined ? parseFloat(amount) : expenses[expenseIndex].amount,
    category: category || expenses[expenseIndex].category,
    date: date || expenses[expenseIndex].date,
  };

  writeExpenses(expenses);
  res.json(expenses[expenseIndex]);
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

// GET expenses by category
app.get('/api/expenses/category/:category', (req, res) => {
  const { category } = req.params;
  const expenses = readExpenses();
  const filtered = expenses.filter(exp => exp.category.toLowerCase() === category.toLowerCase());

  res.json(filtered);
});

// GET expense statistics
app.get('/api/stats/summary', (req, res) => {
  const expenses = readExpenses();

  if (expenses.length === 0) {
    return res.json({
      totalExpenses: 0,
      averageExpense: 0,
      highestExpense: 0,
      lowestExpense: 0,
      byCategory: {},
      count: 0,
    });
  }

  const total = expenses.reduce((sum, exp) => sum + exp.amount, 0);
  const average = total / expenses.length;
  const amounts = expenses.map(exp => exp.amount);
  const highest = Math.max(...amounts);
  const lowest = Math.min(...amounts);

  // Group by category
  const byCategory = {};
  expenses.forEach(exp => {
    if (!byCategory[exp.category]) {
      byCategory[exp.category] = { total: 0, count: 0 };
    }
    byCategory[exp.category].total += exp.amount;
    byCategory[exp.category].count += 1;
  });

  res.json({
    totalExpenses: parseFloat(total.toFixed(2)),
    averageExpense: parseFloat(average.toFixed(2)),
    highestExpense: highest,
    lowestExpense: lowest,
    byCategory,
    count: expenses.length,
  });
});

// ML-powered auto-categorization
app.post('/api/predict-category', async (req, res) => {
  try {
    const { description } = req.body;

    if (!description) {
      return res.status(400).json({ error: 'Description is required' });
    }

    // Call the Python ML server
    const response = await axios.post(`${ML_SERVER_URL}/api/predict-category`, {
      description: description
    });

    res.json(response.data);
  } catch (error) {
    console.error('Error calling ML server:', error.message);
    // Fallback to a simple default category if ML server is unavailable
    res.status(503).json({ 
      error: 'ML service unavailable',
      fallback: true,
      category: 'Other'
    });
  }
});

// Get available categories
app.get('/api/categories', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVER_URL}/api/categories`);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching categories:', error.message);
    // Fallback categories
    res.json({ 
      categories: ['Food', 'Transport', 'Utilities', 'Entertainment', 'Shopping', 'Other'] 
    });
  }
});

// Monthly expense prediction
app.get('/api/monthly-prediction', (req, res) => {
  try {
    // Use Python to calculate prediction
    const options = {
      mode: 'json',
      pythonPath: 'python',
      pythonOptions: ['-u'],
      scriptPath: __dirname,
      args: []
    };

    const pyshell = new PythonShell('get_prediction.py', options);
    
    pyshell.on('message', (message) => {
      if (message && message.success !== undefined) {
        res.json(message);
      }
    });

    pyshell.on('error', (err) => {
      console.error('Prediction error:', err);
      res.status(500).json({ 
        error: 'Could not generate prediction',
        fallback: {
          success: false,
          message: 'Prediction requires at least 2 months of data'
        }
      });
    });

    pyshell.end((err) => {
      if (err) {
        console.error('Python shell error:', err);
        res.status(500).json({ error: 'Prediction service unavailable' });
      }
    });
  } catch (error) {
    console.error('Prediction endpoint error:', error);
    res.status(500).json({ error: 'Failed to generate prediction' });
  }
});

// Expense trends (last 6 months)
app.get('/api/expense-trends', (req, res) => {
  try {
    const options = {
      mode: 'json',
      pythonPath: 'python',
      pythonOptions: ['-u'],
      scriptPath: __dirname,
      args: []
    };

    const pyshell = new PythonShell('get_trends.py', options);
    
    pyshell.on('message', (message) => {
      if (Array.isArray(message) || (message && message.trends)) {
        res.json(Array.isArray(message) ? { trends: message } : message);
      }
    });

    pyshell.on('error', (err) => {
      console.error('Trends error:', err);
      res.status(500).json({ error: 'Could not fetch trends' });
    });

    pyshell.end((err) => {
      if (err) {
        console.error('Python shell error:', err);
        res.status(500).json({ error: 'Trends service unavailable' });
      }
    });
  } catch (error) {
    console.error('Trends endpoint error:', error);
    res.status(500).json({ error: 'Failed to fetch trends' });
  }
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
