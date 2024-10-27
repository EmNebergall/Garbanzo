import { useState, useEffect } from 'react';
import { fetchTransactions } from '../services/api';

export const useTransactions = (dateRange) => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadTransactions = async () => {
      try {
        setLoading(true);
        const data = await fetchTransactions(dateRange);
        setTransactions(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    loadTransactions();
  }, [dateRange]);

  return { transactions, loading, error };
};