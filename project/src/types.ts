export interface Item {
  id: string;
  name: string;
  email: string;
  category: string;
  status: string;
  date: string;
  description: string;
}

export interface FilterState {
  search: string;
  category: string;
  status: string;
  dateRange: {
    start: string;
    end: string;
  };
}