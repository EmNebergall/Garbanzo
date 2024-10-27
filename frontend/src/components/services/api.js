const API_BASE_URL = 'http://localhost:5000/api';

export const fetchTransactions = async (dateRange) => {
  const response = await fetch(
    `${API_BASE_URL}/transactions?start=${dateRange.start}&end=${dateRange.end}`
  );
  return response.json();
};

export const fetchMonthlySummary = async () => {
  const response = await fetch(`${API_BASE_URL}/monthly-summary`);
  return response.json();
};

export const fetchCategories = async () => {
  const response = await fetch(`${API_BASE_URL}/categories`);
  return response.json();
};