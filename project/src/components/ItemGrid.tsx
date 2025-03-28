import React from 'react';
import { Mail } from 'lucide-react';
import { Item } from '../types';

interface ItemGridProps {
  items: Item[];
}

export const ItemGrid: React.FC<ItemGridProps> = ({ items }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {items.map((item) => (
        <div
          key={item.id}
          className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-lg font-semibold text-gray-900">{item.name}</h3>
            <span className={`px-2 py-1 rounded-full text-sm ${
              item.status === 'Active' ? 'bg-green-100 text-green-800' :
              item.status === 'Available' ? 'bg-blue-100 text-blue-800' :
              'bg-yellow-100 text-yellow-800'
            }`}>
              {item.status}
            </span>
          </div>
          
          <p className="text-gray-600 mb-4">{item.description}</p>
          
          <div className="flex flex-col gap-2 text-sm text-gray-500">
            <div>Category: {item.category}</div>
            <div>Date: {new Date(item.date).toLocaleDateString()}</div>
            <a
              href={`mailto:${item.email}`}
              className="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors"
            >
              <Mail className="h-4 w-4" />
              {item.email}
            </a>
          </div>
        </div>
      ))}
    </div>
  );
};