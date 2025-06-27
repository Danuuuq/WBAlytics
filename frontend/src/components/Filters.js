import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';

const Filters = ({ filters, setFilters, categories }) => {
  const [priceRange, setPriceRange] = useState([0, 100_000]);

  // Применяем слайдер к фильтрам
  useEffect(() => {
    setFilters((prev) => ({
      ...prev,
      min_price: priceRange[0],
      max_price: priceRange[1],
    }));
  }, [priceRange]);

  const handleChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const categoryOptions = categories.map((cat) => ({
    value: cat.name,
    label: cat.name,
  }));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ maxWidth: 300 }}>
        <Select
          options={categoryOptions}
          placeholder="Выберите категорию..."
          onChange={(selected) => handleChange('query', selected?.value)}
          isClearable
          isSearchable
        />
      </div>

      <div>
        <label>Диапазон цен: {priceRange[0]} ₽ – {priceRange[1]} ₽</label>
        <Slider
          range
          min={0}
          max={200000}
          step={500}
          value={priceRange}
          onChange={(value) => setPriceRange(value)}
        />
      </div>

      <input
        type="number"
        placeholder="Мин. рейтинг"
        step="0.1"
        value={filters.min_rating || ''}
        onChange={(e) => handleChange('min_rating', e.target.value)}
      />
      <input
        type="number"
        placeholder="Мин. отзывов"
        value={filters.min_reviews || ''}
        onChange={(e) => handleChange('min_reviews', e.target.value)}
      />
    </div>
  );
};

export default Filters;
