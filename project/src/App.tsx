import React, { useState, useMemo } from 'react';
import { SearchBar } from './components/SearchBar';
import { Filters } from './components/Filters';
import { ItemGrid } from './components/ItemGrid';
import { FilterState, Item } from './types';
import { mockData } from './data';

function App() {
  const [filters, setFilters] = useState<FilterState>({
    search: '',
    category: '',
    status: '',
    dateRange: {
      start: '',
      end: ''
    }
  });

  const filteredItems = useMemo(() => {
    return mockData.filter((item: Item) => {
      // Search filter
      const searchTerm = filters.search.toLowerCase();
      const matchesSearch = !searchTerm || 
        Object.values(item).some(value => 
          value.toString().toLowerCase().includes(searchTerm)
        );

      // Category filter
      const matchesCategory = !filters.category || 
        item.category === filters.category;

      // Status filter
      const matchesStatus = !filters.status || 
        item.status === filters.status;

      // Date range filter
      const itemDate = new Date(item.date);
      const matchesDateRange = (
        (!filters.dateRange.start || itemDate >= new Date(filters.dateRange.start)) &&
        (!filters.dateRange.end || itemDate <= new Date(filters.dateRange.end))
      );

      return matchesSearch && matchesCategory && matchesStatus && matchesDateRange;
    });
  }, [filters]);

  const handleReset = () => {
    setFilters({
      search: '',
      category: '',
      status: '',
      dateRange: {
        start: '',
        end: ''
      }
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="bg-white rounded-xl shadow-sm p-6 space-y-6">
          <h1 className="text-2xl font-bold text-gray-900">Item Directory</h1>
          
          <SearchBar
            value={filters.search}
            onChange={(value) => setFilters({ ...filters, search: value })}
          />
          
          <Filters
            filters={filters}
            onFilterChange={setFilters}
            onReset={handleReset}
          />
        </div>

        <div className="mt-8">
          {filteredItems.length > 0 ? (
            <ItemGrid items={filteredItems} />
          ) : (
            <div className="text-center py-12 bg-white rounded-xl shadow-sm">
              <p className="text-gray-500">No items found matching your criteria.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;