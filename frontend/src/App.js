import React, { useEffect, useState } from 'react';
import { fetchProducts, fetchCategories } from './api';
import Filters from './components/Filters';
import ProductTable from './components/ProductTable';
import ChartsPage from './components/ChartsPage';

function App() {
  const [filters, setFilters] = useState({});
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [sortBy, setSortBy] = useState({ field: 'price', direction: 'asc' });
  const [view, setView] = useState('table');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCategories().then(setCategories);
  }, []);

  useEffect(() => {
    if (!filters.query) return;
    setLoading(true);
    const timeout = setTimeout(() => {
      fetchProducts(filters)
        .then(setProducts)
        .finally(() => setLoading(false));
    }, 100);
    return () => clearTimeout(timeout);
  }, [filters]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Аналитика товаров Wildberries</h1>

      <div style={{ marginBottom: 20 }}>
        <button onClick={() => setView('table')} disabled={view === 'table'}>
          📋 Таблица
        </button>
        <button onClick={() => setView('charts')} disabled={view === 'charts'} style={{ marginLeft: 10 }}>
          📈 Диаграммы
        </button>
      </div>

      <Filters filters={filters} setFilters={setFilters} categories={categories} />

      {loading && (
        <div style={{ margin: '20px 0', color: '#555' }}>
          🔄 Загрузка данных...
        </div>
      )}

      {view === 'table' && (
        <ProductTable products={products} sortBy={sortBy} setSortBy={setSortBy} setFilters={setFilters} />
      )}
      {view === 'charts' && (
        <ChartsPage products={products} />
      )}
    </div>
  );
}

export default App;
