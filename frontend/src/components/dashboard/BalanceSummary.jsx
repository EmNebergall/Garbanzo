import { Card } from '@/components/ui/card';

export default function BalanceSummary({ data }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card className="p-4">
        <h3 className="text-lg font-medium">Total Income</h3>
        <p className="text-2xl font-bold text-green-600">
          ${data.income.toFixed(2)}
        </p>
      </Card>
      <Card className="p-4">
        <h3 className="text-lg font-medium">Total Expenses</h3>
        <p className="text-2xl font-bold text-red-600">
          ${data.expenses.toFixed(2)}
        </p>
      </Card>
      <Card className="p-4">
        <h3 className="text-lg font-medium">Net Balance</h3>
        <p className="text-2xl font-bold">
          ${(data.income - data.expenses).toFixed(2)}
        </p>
      </Card>
    </div>
  );
}