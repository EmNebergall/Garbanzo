import { Table } from '@/components/ui/table';
import { formatDate, formatAmount } from '../../utils/formatters';

export default function TransactionList({ transactions }) {
  return (
    <Table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Description</th>
          <th>Category</th>
          <th>Amount</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((transaction) => (
          <tr key={transaction.id}>
            <td>{formatDate(transaction.date)}</td>
            <td>{transaction.description}</td>
            <td>{transaction.category}</td>
            <td className={
              transaction.amount < 0 ? 'text-red-600' : 'text-green-600'
            }>
              {formatAmount(transaction.amount)}
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}