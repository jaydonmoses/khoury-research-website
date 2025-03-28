import React from 'react';
import { FilterState } from '../types';

interface FiltersProps {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
  onReset: () => void;
}

export const Filters: React.FC<FiltersProps> = ({ filters, onFilterChange, onReset }) => {
  const categories = ['All', 'Development', 'Design', 'Marketing'];
  const statuses = ['All', 'Active', 'Available', 'Busy'];

  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center">
      <select
        className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        value={filters.category}
        onChange={(e) => onFilterChange({ ...filters, category: e.target.value })}
      >
        {categories.map((category) => (
          <option key={category} value={category === 'All' ? '' : category}>
            {category}
          </option>
        ))}
      </select>

      <select
        className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        value={filters.status}
        onChange={(e) => onFilterChange({ ...filters, status: e.target.value })}
      >
        {statuses.map((status) => (
          <option key={status} value={status === 'All' ? '' : status}>
            {status}
          </option>
        ))}
      </select>

      <div className="flex gap-2">
        <input
          type="date"
          className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          value={filters.dateRange.start}
          onChange={(e) => onFilterChange({
            ...filters,
            dateRange: { ...filters.dateRange, start: e.target.value }
          })}
        />
        <input
          type="date"
          className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          value={filters.dateRange.end}
          onChange={(e) => onFilterChange({
            ...filters,
            dateRange: { ...filters.dateRange, end: e.target.value }
          })}
        />
      </div>

      <button
        onClick={onReset}
        className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
      >
        Reset Filters
      </button>
    </div>
  );
};