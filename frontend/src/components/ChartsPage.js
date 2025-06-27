import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer,
  LineChart, Line, Legend, Label, Tooltip,
} from 'recharts';

function ChartsPage({ products }) {
  const getPriceBuckets = () => {
    if (!products.length) return [];

    const maxPrice = Math.max(...products.map(p => p.price || 0));
    const step = Math.ceil(maxPrice / 20);
    const buckets = {};

    for (let i = 0; i <= maxPrice; i += step) {
      const rangeLabel = `${i}–${i + step}`;
      buckets[rangeLabel] = 0;
    }

    products.forEach((p) => {
      const price = p.price;
      for (let i = 0; i <= maxPrice; i += step) {
        if (price >= i && price < i + step) {
          const rangeLabel = `${i}–${i + step}`;
          buckets[rangeLabel]++;
          break;
        }
      }
    });

    return Object.entries(buckets)
      .filter(([, count]) => count > 0)
      .map(([range, count]) => ({ range, count }));
  };

  const discountVsRating = products.map((p) => ({
    rating: p.rating,
    discount: parseFloat((p.price - p.discounted_price).toFixed(2)),
  })).filter(p => p.rating && p.discount >= 0);

  const priceVsRating = products.map((p) => ({
    rating: p.rating,
    price: p.price,
  })).filter(p => p.rating && p.price);

  return (
    <div style={{ marginTop: 40 }}>
      <h2>Гистограмма: Цена → Кол-во товаров</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={getPriceBuckets()} margin={{ top: 20, right: 30, bottom: 40, left: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="range" interval={0} angle={-40} textAnchor="end" height={80}>
            <Label value="Диапазон цен (₽)" offset={0} position="insideBottom" />
          </XAxis>
          <YAxis allowDecimals={false}>
            <Label angle={-90} position="insideLeft" style={{ textAnchor: 'middle' }}>
              Кол-во товаров
            </Label>
          </YAxis>
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#8884d8" name="Товары" />
        </BarChart>
      </ResponsiveContainer>

      <h2 style={{ marginTop: 40 }}>📉 График: Скидка vs Рейтинг</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={discountVsRating} margin={{ top: 20, right: 30, bottom: 40, left: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="rating">
            <Label value="Рейтинг" offset={-10} position="insideBottom" />
          </XAxis>
          <YAxis>
            <Label angle={-90} position="insideLeft" style={{ textAnchor: 'middle' }}>
              Скидка (₽)
            </Label>
          </YAxis>
          <Tooltip formatter={(v) => `${v}₽`} />
          <Legend />
          <Line type="monotone" dataKey="discount" stroke="#82ca9d" dot={{ r: 3 }} name="Скидка" />
        </LineChart>
      </ResponsiveContainer>

      <h2 style={{ marginTop: 40 }}>📈 График: Цена vs Рейтинг</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={priceVsRating} margin={{ top: 20, right: 30, bottom: 40, left: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="rating">
            <Label value="Рейтинг" offset={-10} position="insideBottom" />
          </XAxis>
          <YAxis>
            <Label angle={-90} position="insideLeft" style={{ textAnchor: 'middle' }}>
              Цена (₽)
            </Label>
          </YAxis>
          <Tooltip formatter={(v) => `${v}₽`} />
          <Legend />
          <Line type="monotone" dataKey="price" stroke="#8884d8" dot={{ r: 3 }} name="Цена" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ChartsPage;
